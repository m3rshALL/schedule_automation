from django.contrib import admin
from .models import Course, Subject, StudentGroup

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "student_group", "hours_per_week", "course_year", "lesson_type", "is_mook")
    list_filter = ("course_year", "lesson_type", "is_mook")
    search_fields = ("subject__name", "student_group__name")

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")
    search_fields = ("name", "code")

@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "size")
    search_fields = ("name",)
