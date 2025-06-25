from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import optimize_schedule_task

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
