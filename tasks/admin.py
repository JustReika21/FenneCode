from django.contrib import admin

from tasks.models import ChoiceTask, Answer


@admin.register(ChoiceTask)
class ChoiceTaskAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'question', 'question_type')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('choice_task', 'answer', 'is_correct')
