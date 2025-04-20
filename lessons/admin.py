from django.contrib import admin

from lessons.models import Lesson, LessonContent


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'position')


@admin.register(LessonContent)
class LessonContentAdmin(admin.ModelAdmin):
    list_display = ('type', 'content')