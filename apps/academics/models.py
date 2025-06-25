from django.db import models
from django.utils.translation import gettext_lazy as _


class Subject(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    code = models.CharField(_("Subject Code"), max_length=20, unique=True)

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return f"{self.name} ({self.code})"


class StudentGroup(models.Model):
    name = models.CharField(_("Group Name"), max_length=255, unique=True)
    size = models.PositiveIntegerField(_("Number of Students"))

    class Meta:
        verbose_name = _("Student Group")
        verbose_name_plural = _("Student Groups")

    def __str__(self):
        return self.name


class Course(models.Model):
    subject = models.ForeignKey(
        "academics.Subject", on_delete=models.CASCADE, related_name="courses"
    )
    student_group = models.ForeignKey(
        "academics.StudentGroup", on_delete=models.CASCADE, related_name="courses"
    )
    hours_per_week = models.PositiveIntegerField(
        _("Hours per Week"), help_text=_("Number of hours the course is held per week.")
    )
    required_equipment = models.ManyToManyField(
        "facilities.Equipment",
        verbose_name=_("Required Equipment"),
        blank=True,
    )
    
    # Новые поля для интеграции с OptaPy
    COURSE_YEAR_CHOICES = [
        (1, _("1st year")),
        (2, _("2nd year")),
        (3, _("3rd year")),
    ]
    course_year = models.PositiveSmallIntegerField(
        _("Course Year"),
        choices=COURSE_YEAR_CHOICES,
        default=1,
        help_text=_("Year of study: 1, 2, or 3")
    )
    LESSON_TYPE_CHOICES = [
        ("lecture", _("Lecture")),
        ("practice", _("Practice")),
        ("lab", _("Laboratory")),
        ("mook", _("MOOK/Online")),
    ]
    lesson_type = models.CharField(
        max_length=16,
        choices=LESSON_TYPE_CHOICES,
        default="lecture",
        verbose_name=_("Lesson Type"),
        help_text=_("Type of lesson: lecture, practice, lab, mook")
    )
    is_mook = models.BooleanField(
        _("Is MOOK (Online)"),
        default=False,
        help_text=_("Is this lesson a MOOK/online lesson?")
    )
    is_elective = models.BooleanField(
        _("Is Elective"),
        default=False,
        help_text=_("Is this course an elective?")
    )
    elective_group = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name=_('Elective Group'),
        help_text=_('Identifier for grouping elective courses')
    )
    parent_course = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Parent Course'),
        help_text=_('Link to parent course for lecture/seminar/practice sequence'),
        related_name='child_courses'
    )

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        unique_together = ("subject", "student_group")

    def __str__(self):
        return f"{self.subject} for {self.student_group}"
