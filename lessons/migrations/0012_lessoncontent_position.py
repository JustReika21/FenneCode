# Generated by Django 5.1.6 on 2025-04-20 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0011_remove_lesson_content_lessoncontent_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessoncontent',
            name='position',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
