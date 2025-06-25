from optapy import constraint_provider
from optapy.score import HardSoftScore
from optapy.types import Joiners

from .optapy_entities import ScheduleEntry

@constraint_provider
def define_constraints(constraint_factory):
    constraints = []

    # 1. Конфликт преподавателей: один преподаватель не может вести два занятия одновременно
    constraints.append(
        constraint_factory.for_each_unique_pair(
            ScheduleEntry(),
            Joiners.equal(lambda entry: entry.teacher.id),
            Joiners.equal(lambda entry: entry.timeslot)
        ).penalize(
            "Teacher conflict",
            HardSoftScore.ONE_HARD
        )
    )

    # 2. Конфликт аудиторий: одна аудитория не может использоваться для двух занятий одновременно
    constraints.append(
        constraint_factory.for_each_unique_pair(
            ScheduleEntry(),
            Joiners.equal(lambda entry: entry.room.id),
            Joiners.equal(lambda entry: entry.timeslot)
        ).penalize(
            "Room conflict",
            HardSoftScore.ONE_HARD
        )
    )

    # 3. Лимит часов в день для преподавателей (не более 8)
    # (Группы реализуются аналогично, если добавить поле group в ScheduleEntry)
    # Здесь только пример для преподавателей:
    constraints.append(
        constraint_factory.for_each(ScheduleEntry())
        .group_by(
            lambda entry: (entry.teacher.id, entry.timeslot.day),
            lambda entries: len(entries)
        )
        .filter(lambda key, count: count > 8)
        .penalize(
            "Teacher daily hour limit",
            HardSoftScore.ONE_HARD,
            lambda key, count: count - 8
        )
    )

    # 4. Лимит часов в день для групп (не более 8)
    constraints.append(
        constraint_factory.for_each(ScheduleEntry())
        .group_by(
            lambda entry: (entry.student_group_id, entry.timeslot.day),
            lambda entries: len(entries)
        )
        .filter(lambda key, count: count > 8)
        .penalize(
            "Student group daily hour limit",
            HardSoftScore.ONE_HARD,
            lambda key, count: count - 8
        )
    )

    # 5. Смены по курсам (ограничение по времени и дням недели)
    # 1 курс: ПН-СБ, 08:00-14:00; 2 курс: ПН-ПТ, 13:00-20:00; 3 курс: ПН-СБ (кроме ЧТ), 08:00-14:00
    def is_shift_violation(entry):
        if entry.course_year == 1:
            if entry.timeslot.day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
                return True
            if not ("08:00" <= entry.timeslot.start_time <= "14:00"):
                return True
        elif entry.course_year == 2:
            if entry.timeslot.day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                return True
            if not ("13:00" <= entry.timeslot.start_time <= "20:00"):
                return True
        elif entry.course_year == 3:
            if entry.timeslot.day not in ["Monday", "Tuesday", "Wednesday", "Friday", "Saturday"]:
                return True
            if not ("08:00" <= entry.timeslot.start_time <= "14:00"):
                return True
        return False
    constraints.append(
        constraint_factory.for_each(ScheduleEntry())
        .filter(is_shift_violation)
        .penalize("Shift violation by course year", HardSoftScore.ONE_HARD)
    )

    # 6. Военная кафедра: блокировка дней для 2 и 3 курса
    def is_military_block(entry):
        # 2 курс: суббота (Saturday) запрещено; 3 курс: четверг (Thursday) запрещено
        if entry.course_year == 2 and entry.timeslot.day == "Saturday":
            return True
        if entry.course_year == 3 and entry.timeslot.day == "Thursday":
            return True
        return False
    constraints.append(
        constraint_factory.for_each(ScheduleEntry())
        .filter(is_military_block)
        .penalize("Military department block", HardSoftScore.ONE_HARD)
    )

    # 7. MOOK занятия: должны быть с отрывом 2 часа от других занятий группы
    # (упрощённая версия: не должно быть других занятий в течение 2 часов до/после)
    def mook_time_conflict(entry1, entry2):
        if not entry1.is_mook or entry1.student_group_id != entry2.student_group_id:
            return False
        # Проверяем разницу во времени между занятиями
        t1 = int(entry1.timeslot.start_time[:2]) * 60 + int(entry1.timeslot.start_time[3:])
        t2 = int(entry2.timeslot.start_time[:2]) * 60 + int(entry2.timeslot.start_time[3:])
        return abs(t1 - t2) < 120 and entry1.timeslot.day == entry2.timeslot.day and entry1.id != entry2.id
    constraints.append(
        constraint_factory.for_each_unique_pair(ScheduleEntry())
        .filter(mook_time_conflict)
        .penalize("MOOK 2-hour gap violation", HardSoftScore.ONE_HARD)
    )

    # 8. Последовательность занятий: 2 подряд одного типа — должны идти подряд; 3 занятия — 2 подряд, 1 отдельно
    # (упрощённая версия: если есть 2 занятия одного типа в один день — они должны идти подряд)
    def not_sequential(entry1, entry2):
        if entry1.lesson_type != entry2.lesson_type:
            return False
        if entry1.student_group_id != entry2.student_group_id:
            return False
        if entry1.timeslot.day != entry2.timeslot.day:
            return False
        t1 = int(entry1.timeslot.start_time[:2]) * 60 + int(entry1.timeslot.start_time[3:])
        t2 = int(entry2.timeslot.start_time[:2]) * 60 + int(entry2.timeslot.start_time[3:])
        return abs(t1 - t2) > 90 and entry1.id != entry2.id  # не подряд
    constraints.append(
        constraint_factory.for_each_unique_pair(ScheduleEntry())
        .filter(not_sequential)
        .penalize("Lesson sequence violation", HardSoftScore.ONE_HARD)
    )

    # Пример шаблона для ограничения по смене (1 курс):
    # constraints.append(
    #     constraint_factory.for_each(ScheduleEntry())
    #     .filter(lambda entry: entry.course_year == 1 and not (
    #         entry.timeslot.day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] and
    #         entry.timeslot.start_time >= "08:00" and entry.timeslot.end_time <= "14:00"
    #     ))
    #     .penalize("1st year shift violation", HardSoftScore.ONE_HARD)
    # )

    # Аналогично для военной кафедры и MOOK — требуется расширение данных

    # --- МЯГКИЕ ОГРАНИЧЕНИЯ ---
    # 1. Минимизировать окна у групп и преподавателей
    def has_gap(entry1, entry2):
        if entry1.student_group_id != entry2.student_group_id and entry1.teacher.id != entry2.teacher.id:
            return False
        if entry1.timeslot.day != entry2.timeslot.day:
            return False
        t1 = int(entry1.timeslot.start_time[:2]) * 60 + int(entry1.timeslot.start_time[3:])
        t2 = int(entry2.timeslot.start_time[:2]) * 60 + int(entry2.timeslot.start_time[3:])
        return 0 < abs(t1 - t2) < 90  # окно менее 1.5 часа
    constraints.append(
        constraint_factory.for_each_unique_pair(ScheduleEntry())
        .filter(has_gap)
        .penalize("Minimize gaps for groups and teachers", HardSoftScore.ONE_SOFT)
    )

    # 2. Допустимое превышение вместимости аудиторий на 2-3 единицы
    def room_capacity_soft(entry):
        if entry.room.capacity + 3 >= entry.course.student_group_id:  # student_group_id как proxy для размера
            return False
        return True
    constraints.append(
        constraint_factory.for_each(ScheduleEntry())
        .filter(room_capacity_soft)
        .penalize("Room capacity soft overflow", HardSoftScore.ONE_SOFT)
    )

    # 3. Оставить по одному окну до/после занятия в другом блоке (где аудитория не C1)
    def block_gap(entry1, entry2):
        if entry1.student_group_id != entry2.student_group_id:
            return False
        if entry1.room.block == "C1" or entry2.room.block == "C1":
            return False
        if entry1.timeslot.day != entry2.timeslot.day:
            return False
        t1 = int(entry1.timeslot.start_time[:2]) * 60 + int(entry1.timeslot.start_time[3:])
        t2 = int(entry2.timeslot.start_time[:2]) * 60 + int(entry2.timeslot.start_time[3:])
        return abs(t1 - t2) == 90  # ровно одно окно между занятиями
    constraints.append(
        constraint_factory.for_each_unique_pair(ScheduleEntry())
        .filter(block_gap)
        .penalize("Block gap for non-C1 rooms", HardSoftScore.ONE_SOFT)
    )

    # 4. Элективные потоки одновременно у лекционных и семинарских потоков
    def elective_parallel(entry1, entry2):
        if not entry1.is_elective or not entry2.is_elective:
            return False
        if entry1.elective_group != entry2.elective_group or not entry1.elective_group:
            return False
        if entry1.timeslot.day != entry2.timeslot.day:
            return False
        return entry1.timeslot.start_time != entry2.timeslot.start_time
    constraints.append(
        constraint_factory.for_each_unique_pair(ScheduleEntry())
        .filter(elective_parallel)
        .penalize("Elective streams not scheduled in parallel", HardSoftScore.ONE_SOFT)
    )

    # 5. Лекции перед семинарами (если 3 лекции — практики между ними)
    def lecture_before_seminar(entry1, entry2):
        if entry1.parent_course_id != entry2.parent_course_id or not entry1.parent_course_id:
            return False
        if entry1.lesson_type == "lecture" and entry2.lesson_type == "practice":
            # Лекция должна быть раньше практики
            if entry1.timeslot.day != entry2.timeslot.day:
                return False
            t1 = int(entry1.timeslot.start_time[:2]) * 60 + int(entry1.timeslot.start_time[3:])
            t2 = int(entry2.timeslot.start_time[:2]) * 60 + int(entry2.timeslot.start_time[3:])
            return t1 > t2
        return False
    constraints.append(
        constraint_factory.for_each_unique_pair(ScheduleEntry())
        .filter(lecture_before_seminar)
        .penalize("Lecture should be before practice", HardSoftScore.ONE_SOFT)
    )

    # 6. Занятия по одной дисциплине не должны идти два дня подряд
    def not_consecutive_days(entry1, entry2):
        if entry1.course.subject_id != entry2.course.subject_id:
            return False
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        try:
            idx1 = days.index(entry1.timeslot.day)
            idx2 = days.index(entry2.timeslot.day)
        except ValueError:
            return False
        return abs(idx1 - idx2) == 1
    constraints.append(
        constraint_factory.for_each_unique_pair(ScheduleEntry())
        .filter(not_consecutive_days)
        .penalize("No consecutive days for same subject", HardSoftScore.ONE_SOFT)
    )

    return constraints 