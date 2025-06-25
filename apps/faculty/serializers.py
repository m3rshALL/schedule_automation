from rest_framework import serializers

from apps.academics.models import Subject
from apps.academics.serializers import SubjectSerializer

from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    qualifications = SubjectSerializer(many=True, read_only=True)
    qualification_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Subject.objects.all(),
        source="qualifications",
        write_only=True,
    )

    class Meta:
        model = Teacher
        fields = (
            "id",
            "name",
            "qualifications",
            "qualification_ids",
        ) 