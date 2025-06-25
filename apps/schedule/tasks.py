from celery import shared_task
from apps.academics.models import Course
from apps.faculty.models import Teacher
from apps.facilities.models import Room
from apps.schedule.models import TimeSlot, Schedule
from utils.optapy_transform import course_to_fact, teacher_to_fact, room_to_fact, timeslot_to_fact

@shared_task
def optimize_schedule_task():
    """
    Celery-задача для запуска OptaPy-оптимизации расписания.
    """
    # 1. Получить все необходимые данные
    courses = list(Course.objects.all())
    teachers = list(Teacher.objects.all())
    rooms = list(Room.objects.all())
    timeslots = list(TimeSlot.objects.all())

    # 2. Преобразовать в OptaPy DTO
    course_facts = [course_to_fact(c) for c in courses]
    teacher_facts = [teacher_to_fact(t) for t in teachers]
    room_facts = [room_to_fact(r) for r in rooms]
    timeslot_facts = [timeslot_to_fact(ts) for ts in timeslots]

    # 3. Сформировать planning entities (ScheduleEntry) и solution
    # TODO: реализовать генерацию ScheduleEntry и запуск OptaPy solver
    # from apps.schedule.optapy_entities import ScheduleSolution
    # solution = ScheduleSolution(...)
    # result = solve_with_optapy(solution)

    # 4. Сохранить результат в Schedule
    # TODO: очистить старое расписание и записать новое
    # for entry in result.schedule_entries:
    #     Schedule.objects.create(...)

    return "Optimization started (mock)" 