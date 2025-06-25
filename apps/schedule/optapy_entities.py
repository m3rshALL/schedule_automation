from dataclasses import dataclass, field
from typing import List, Optional
from optapy import (
    planning_entity,
    planning_solution,
    planning_variable,
    value_range_provider,
    problem_fact,
    problem_fact_collection_property
)
from optapy.score import HardSoftScore

@problem_fact
@dataclass(frozen=True)
class TimeSlotFact:
    """Временной слот для занятия (день недели, время начала и конца)"""
    id: int
    day: str
    start_time: str  # '08:00'
    end_time: str    # '09:30'

    def __str__(self):
        return f"TimeSlotFact({self.day} {self.start_time}-{self.end_time})"

@problem_fact
@dataclass(frozen=True)
class RoomFact:
    """Аудитория: id, название, вместимость, тип, оборудование, блок"""
    id: int
    name: str
    capacity: int
    room_type: str
    equipment: List[str]
    block: str  # Новый признак блока

    def __str__(self):
        return f"RoomFact({self.name}, Cap:{self.capacity}, Type:{self.room_type})"

@problem_fact
@dataclass(frozen=True)
class TeacherFact:
    """Преподаватель: id, ФИО, список id дисциплин"""
    id: int
    name: str
    qualifications: List[int]  # subject ids

    def __str__(self):
        return f"TeacherFact({self.name})"

@problem_fact
@dataclass(frozen=True)
class CourseFact:
    """Курс/дисциплина для планирования занятия"""
    id: int
    subject_id: int
    student_group_id: int
    hours_per_week: int
    required_equipment: List[str]
    course_year: int    # Год обучения (1, 2, 3)
    lesson_type: str    # Тип занятия (лекция, практика, лабораторная)
    is_mook: bool       # Признак MOOK (онлайн-лекция)
    is_elective: bool   # Признак электива
    elective_group: str # Группа электива
    parent_course_id: Optional[int] = None # id родительского курса (или None). Использовать Optional для None.

    def __str__(self):
        return f"CourseFact(id={self.id}, Subj:{self.subject_id}, Group:{self.student_group_id})"


# ----------------------------------------------------------------------
# Planning Entity (Планируемая сущность - объект, который OptaPy будет перемещать)
# ----------------------------------------------------------------------

@planning_entity
@dataclass
class ScheduleEntry:
    """Планируемое занятие: связь курса, преподавателя, группы, переменные timeslot и room"""
    id: int
    course: CourseFact
    teacher: TeacherFact # Teacher is also a fact, it's assigned to a ScheduleEntry
    student_group_id: int
    # Дублируем для constraints (быстрый доступ) - Хорошая идея для оптимизации производительности констрейнтов
    course_year: int
    lesson_type: str
    is_mook: bool
    is_elective: bool
    elective_group: str
    parent_course_id: Optional[int] = None # Опять же, используйте Optional для None

    # Planning variables - переменные, которые OptaPy будет оптимизировать
    # Указываем тип переменной и 'value_range_id' для поиска допустимых значений
    # display_name УДАЛЕН отсюда
    timeslot: Optional[TimeSlotFact] = planning_variable(TimeSlotFact, ['timeslot_range'])
    room: Optional[RoomFact] = planning_variable(RoomFact, ['room_range'])

    def __str__(self):
        return (f"ScheduleEntry(id={self.id}, Course:{self.course.subject_id}, "
                f"Group:{self.student_group_id}, Teacher:{self.teacher.name}, "
                f"Time:{self.timeslot.start_time if self.timeslot else 'N/A'}, "
                f"Room:{self.room.name if self.room else 'N/A'})")

# ----------------------------------------------------------------------
# Solution (Решение - объект, содержащий все сущности и факты задачи)
# ----------------------------------------------------------------------

@planning_solution
@dataclass
class ScheduleSolution:
    # planning_entities - объекты, которые OptaPy будет перемещать и назначать значения
    schedule_entries: List['ScheduleEntry'] = field(default_factory=list)

    # Value ranges - откуда planning_variable будет брать свои значения
    timeslot_range: List['TimeSlotFact'] = value_range_provider("timeslot_range")
    room_range: List['RoomFact'] = value_range_provider("room_range")

    # Problem facts - неизменяемые данные, используемые в задаче
    teacher_facts: List['TeacherFact'] = problem_fact_collection_property(TeacherFact)
    course_facts: List['CourseFact'] = problem_fact_collection_property(CourseFact)
    time_slot_facts: List['TimeSlotFact'] = problem_fact_collection_property(TimeSlotFact)
    room_facts: List['RoomFact'] = problem_fact_collection_property(RoomFact)


    # score - место, куда OptaPy будет записывать оценку текущего решения
    score: Optional[HardSoftScore] = field(default=None, compare=False)

    def __str__(self):
        return f"ScheduleSolution(entries={len(self.schedule_entries)}, score={self.score})"


# Заготовка для constraints (будет реализована отдельно)
# def define_constraints(constraint_factory):
#     # Пример простого hard constraint: каждое занятие должно иметь room и timeslot
#     return [
#         constraint_factory.for_each(ScheduleEntry)
#             .filter(lambda schedule_entry: schedule_entry.timeslot is None)
#             .penalize("Timeslot must be assigned", HardSoftScore.ONE_HARD),
#         constraint_factory.for_each(ScheduleEntry)
#             .filter(lambda schedule_entry: schedule_entry.room is None)
#             .penalize("Room must be assigned", HardSoftScore.ONE_HARD),
#     ]