from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import optimize_schedule_task
import openpyxl
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from .models import Schedule
from rest_framework import permissions
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Create your views here.

class OptimizeScheduleView(APIView):
    """
    POST /api/schedule/optimize/ — запуск задачи оптимизации
    """
    def post(self, request):
        task = optimize_schedule_task.delay()
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)

class OptimizeScheduleStatusView(APIView):
    """
    GET /api/schedule/optimize/status/?task_id=... — статус задачи
    """
    def get(self, request):
        task_id = request.query_params.get("task_id")
        if not task_id:
            return Response({"error": "task_id required"}, status=status.HTTP_400_BAD_REQUEST)
        result = AsyncResult(task_id)
        return Response({
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.successful() else None
        })

class ScheduleExportView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        export_format = request.query_params.get('format', 'excel')
        schedules = Schedule.objects.select_related(
            'course', 'teacher', 'room', 'timeslot', 'course__subject', 'course__student_group'
        ).all().order_by('timeslot__day', 'timeslot__start_time')
        if export_format == 'pdf':
            return self.export_pdf(schedules)
        return self.export_excel(schedules)

    def export_excel(self, schedules):
        wb = openpyxl.Workbook()
        wb.remove(wb.active)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        day_map = {
            'Monday': 'Понедельник',
            'Tuesday': 'Вторник',
            'Wednesday': 'Среда',
            'Thursday': 'Четверг',
            'Friday': 'Пятница',
            'Saturday': 'Суббота',
            'Sunday': 'Воскресенье',
        }
        for day in days:
            ws = wb.create_sheet(title=day_map.get(day, day))
            headers = [
                'Время', 'Группа', 'Кол-во студентов', 'Дисциплина', 'Преподаватель', 'Email',
                'Аудитория', 'Блок', 'Оборудование', 'Тип занятия'
            ]
            ws.append(headers)
            for cell in ws[1]:
                cell.font = openpyxl.styles.Font(bold=True)
            day_schedules = [s for s in schedules if s.timeslot.day == day]
            for s in sorted(day_schedules, key=lambda x: x.timeslot.start_time):
                equipment = ', '.join([e.name for e in s.room.equipment.all()])
                ws.append([
                    f"{s.timeslot.start_time:%H:%M}-{s.timeslot.end_time:%H:%M}",
                    s.course.student_group.name,
                    s.course.student_group.size,
                    s.course.subject.name,
                    s.teacher.name,
                    getattr(s.teacher, 'email', ''),
                    s.room.name,
                    getattr(s.room, 'block', ''),
                    equipment,
                    s.course.lesson_type,
                ])
            ws.auto_filter.ref = ws.dimensions
            for col in range(1, len(headers) + 1):
                ws.column_dimensions[get_column_letter(col)].width = 18
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=schedule_grouped_by_day.xlsx'
        return response

    def export_pdf(self, schedules):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 40
        p.setFont('Helvetica-Bold', 14)
        p.drawString(40, y, 'Расписание занятий')
        y -= 30
        p.setFont('Helvetica', 10)
        headers = ['Группа', 'Дисциплина', 'Преподаватель', 'Аудитория', 'День', 'Время', 'Тип']
        for i, h in enumerate(headers):
            p.drawString(40 + i*80, y, h)
        y -= 20
        for s in schedules:
            row = [
                s.course.student_group.name,
                s.course.subject.name,
                s.teacher.name,
                s.room.name,
                s.timeslot.day,
                f"{s.timeslot.start_time:%H:%M}-{s.timeslot.end_time:%H:%M}",
                s.course.lesson_type,
            ]
            for i, val in enumerate(row):
                p.drawString(40 + i*80, y, str(val))
            y -= 18
            if y < 60:
                p.showPage()
                y = height - 40
        p.save()
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=schedule.pdf'
        return response
