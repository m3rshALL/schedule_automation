from django.db import models

# Create your models here.

class Equipment(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Наименование оборудования")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"


class Room(models.Model):
    class RoomType(models.TextChoices):
        LECTURE = 'LECTURE', 'Лекционная'
        LABORATORY = 'LAB', 'Лаборатория'
        COMPUTER = 'COMP', 'Компьютерный класс'

    name = models.CharField(max_length=100, verbose_name="Номер/название аудитории")
    capacity = models.PositiveIntegerField(verbose_name="Вместимость")
    room_type = models.CharField(
        max_length=10,
        choices=RoomType.choices,
        verbose_name="Тип аудитории"
    )
    equipment = models.ManyToManyField(
        Equipment,
        blank=True,
        verbose_name="Оборудование"
    )
    block = models.CharField(
        max_length=10,
        verbose_name="Блок здания",
        help_text="Буквенно-цифровой идентификатор блока (например, C1, C2)",
        default="C1"
    )

    def __str__(self):
        return f"{self.name} ({self.get_room_type_display()})"

    class Meta:
        verbose_name = "Аудитория"
        verbose_name_plural = "Аудитории"
