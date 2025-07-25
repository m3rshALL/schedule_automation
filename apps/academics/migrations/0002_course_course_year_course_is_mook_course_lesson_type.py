# Generated by Django 5.2.3 on 2025-06-24 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_year',
            field=models.PositiveSmallIntegerField(choices=[(1, '1st year'), (2, '2nd year'), (3, '3rd year')], default=1, help_text='Year of study: 1, 2, or 3', verbose_name='Course Year'),
        ),
        migrations.AddField(
            model_name='course',
            name='is_mook',
            field=models.BooleanField(default=False, help_text='Is this lesson a MOOK/online lesson?', verbose_name='Is MOOK (Online)'),
        ),
        migrations.AddField(
            model_name='course',
            name='lesson_type',
            field=models.CharField(choices=[('lecture', 'Lecture'), ('practice', 'Practice'), ('lab', 'Laboratory'), ('mook', 'MOOK/Online')], default='lecture', help_text='Type of lesson: lecture, practice, lab, mook', max_length=16, verbose_name='Lesson Type'),
        ),
    ]
