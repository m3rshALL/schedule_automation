from dataclasses import dataclass, field
from typing import List, Optional
from optapy import planning_entity, planning_solution, planning_variable, value_range_provider, problem_fact, problem_fact_collection_property
from optapy.score import HardSoftScore

# Problem Facts
@dataclass(frozen=True)
class TimeSlotFact:
    """Временной слот для занятия (день недели, время начала и конца)"""
    id: int
    day: str
    start_time: str  # '08:00'
    end_time: str    # '09:30'

@dataclass(frozen=True)
class RoomFact:
    """Аудитория: id, название, вместимость, тип, оборудование, блок"""
    id: int
    name: str
    capacity: int
    room_type: str
    equipment: List[str]
    block: str  # Новый признак блока

@dataclass(frozen=True)
class TeacherFact:
    """Преподаватель: id, ФИО, список id дисциплин"""
    id: int
    name: str
    qualifications: List[int]  # subject ids

@dataclass(frozen=True)
class CourseFact:
    """Курс/дисциплина для планирования занятия"""
    id: int
    subject_id: int
    student_group_id: int
    hours_per_week: int
    required_equipment: List[str]
    course_year: int  # Год обучения (1, 2, 3)
    lesson_type: str  # Тип занятия (лекция, практика, лабораторная)
    is_mook: bool     # Признак MOOK (онлайн-лекция)
    is_elective: bool # Признак электива
    elective_group: str # Группа электива
    parent_course_id: int # id родительского курса (или None)

# Planning Entity
@planning_entity
def ScheduleEntry():
    @dataclass
    class _ScheduleEntry:
        """Планируемое занятие: связь курса, преподавателя, группы, переменные timeslot и room"""
        id: int
        course: CourseFact
        teacher: TeacherFact
        student_group_id: int
        # Дублируем для constraints (быстрый доступ)
        course_year: int
        lesson_type: str
        is_mook: bool
        is_elective: bool
        elective_group: str
        parent_course_id: int
        # Planning variables
        timeslot: Optional[TimeSlotFact] = planning_variable(TimeSlotFact, ['timeslot_range'])
        room: Optional[RoomFact] = planning_variable(RoomFact, ['room_range'])
    return _ScheduleEntry

# Solution
@planning_solution
def ScheduleSolution():
    @dataclass
    class _ScheduleSolution:
        schedule_entries: List[ScheduleEntry()] = field(default_factory=list)
        # Value ranges
        timeslot_range: List[TimeSlotFact] = value_range_provider("timeslot_range")
        room_range: List[RoomFact] = value_range_provider("room_range")
        # Problem facts
        teacher_facts: List[TeacherFact] = problem_fact_collection_property()
        course_facts: List[CourseFact] = problem_fact_collection_property()
        score: Optional[HardSoftScore] = None
    return _ScheduleSolution

# Заготовка для constraints (будет реализована отдельно)
# def define_constraints(constraint_factory):
#     ... 