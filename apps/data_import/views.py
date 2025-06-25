from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, parsers
from apps.academics.models import StudentGroup
import openpyxl

# Create your views here.

class StudentGroupImportView(APIView):
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [parsers.MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            wb = openpyxl.load_workbook(file)
            ws = wb.active
            created, updated, errors = 0, 0, []
            for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                name, size = row[:2]
                if not name or not size:
                    errors.append(f'Row {i}: missing name or size')
                    continue
                obj, created_flag = StudentGroup.objects.update_or_create(
                    name=name,
                    defaults={'size': size}
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1
            return Response({
                'created': created,
                'updated': updated,
                'errors': errors
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
