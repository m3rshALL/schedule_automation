from typing import List
from apps.academics.models import Course
from apps.faculty.models import Teacher
from apps.facilities.models import Room, Equipment
from apps.schedule.models import TimeSlot
from apps.schedule.optapy_entities import CourseFact, TeacherFact, RoomFact, TimeSlotFact


def course_to_fact(course: Course) -> CourseFact:
    """
    Преобразует Django-модель Course в OptaPy CourseFact.
    Требует, чтобы у Course были атрибуты: course_year, lesson_type, is_mook, is_elective, elective_group, parent_course.
    """
    return CourseFact(
        id=course.id,
        subject_id=course.subject.id,
        student_group_id=course.student_group.id,
        hours_per_week=course.hours_per_week,
        required_equipment=[eq.name for eq in course.required_equipment.all()],
        course_year=course.course_year,
        lesson_type=course.lesson_type,
        is_mook=course.is_mook,
        is_elective=course.is_elective,
        elective_group=course.elective_group or "",
        parent_course_id=course.parent_course.id if course.parent_course else None,
    )


def teacher_to_fact(teacher: Teacher) -> TeacherFact:
    """
    Преобразует Django-модель Teacher в OptaPy TeacherFact.
    """
    return TeacherFact(
        id=teacher.id,
        name=teacher.name,
        qualifications=[s.id for s in teacher.qualifications.all()]
    )


def room_to_fact(room: Room) -> RoomFact:
    """
    Преобразует Django-модель Room в OptaPy RoomFact.
    """
    return RoomFact(
        id=room.id,
        name=room.name,
        capacity=room.capacity,
        room_type=room.room_type,
        equipment=[eq.name for eq in room.equipment.all()],
        block=room.block,
    )


def timeslot_to_fact(timeslot: TimeSlot) -> TimeSlotFact:
    """
    Преобразует Django-модель TimeSlot в OptaPy TimeSlotFact.
    """
    return TimeSlotFact(
        id=timeslot.id,
        day=timeslot.day,
        start_time=timeslot.start_time.strftime('%H:%M'),
        end_time=timeslot.end_time.strftime('%H:%M'),
    )

# TODO: Добавить функцию для ScheduleEntry, когда будет определён способ генерации всех сущностей для планирования 