from django.contrib import admin
from django.utils.regex_helper import Choice

from tasks.models import CodeTask, ChoiceTask, Submission


@admin.register(CodeTask)
class CodeTaskAdmin(admin.ModelAdmin):
    list_display = ('question', 'lesson')


@admin.register(ChoiceTask)
class ChoiceTaskAdmin(admin.ModelAdmin):
    list_display = ('question', 'lesson')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed')
