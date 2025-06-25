from django.db import models
from django.utils.translation import gettext_lazy as _


class Teacher(models.Model):
    name = models.CharField(_("Full Name"), max_length=255)
    qualifications = models.ManyToManyField(
        "academics.Subject",
        verbose_name=_("Qualifications"),
        help_text=_("Subjects the teacher is qualified to teach."),
        related_name="qualified_teachers",
    )

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return self.name
