from rest_framework import serializers

from .models import Course, StudentGroup, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    student_group = StudentGroupSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), source="subject", write_only=True
    )
    student_group_id = serializers.PrimaryKeyRelatedField(
        queryset=StudentGroup.objects.all(), source="student_group", write_only=True
    )

    class Meta:
        model = Course
        fields = (
            "id",
            "subject",
            "student_group",
            "subject_id",
            "student_group_id",
            "hours_per_week",
            "required_equipment",
            "course_year",
            "lesson_type",
            "is_mook",
            "is_elective",
            "elective_group",
            "parent_course",
        ) 