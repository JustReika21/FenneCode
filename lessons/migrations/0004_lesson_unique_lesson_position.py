# Generated by Django 5.1.6 on 2025-03-29 17:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_duration_course_skill_requirements'),
        ('lessons', '0003_lesson_user_lesson_complete'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='lesson',
            constraint=models.UniqueConstraint(fields=('course', 'position'), name='unique_lesson_position'),
        ),
    ]
