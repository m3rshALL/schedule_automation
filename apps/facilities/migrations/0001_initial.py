# Generated by Django 5.2.3 on 2025-06-21 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование оборудования')),
            ],
            options={
                'verbose_name': 'Оборудование',
                'verbose_name_plural': 'Оборудование',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Номер/название аудитории')),
                ('capacity', models.PositiveIntegerField(verbose_name='Вместимость')),
                ('room_type', models.CharField(choices=[('LECTURE', 'Лекционная'), ('LAB', 'Лаборатория'), ('COMP', 'Компьютерный класс')], max_length=10, verbose_name='Тип аудитории')),
                ('equipment', models.ManyToManyField(blank=True, to='facilities.equipment', verbose_name='Оборудование')),
            ],
            options={
                'verbose_name': 'Аудитория',
                'verbose_name_plural': 'Аудитории',
            },
        ),
    ]
