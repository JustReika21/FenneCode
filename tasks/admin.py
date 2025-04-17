from django.contrib import admin

from tasks.models import ChoiceTask, Answer, UserChoiceAnswer


@admin.register(ChoiceTask)
class ChoiceTaskAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'question')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('choice_task', 'answer', 'is_correct')


@admin.register(UserChoiceAnswer)
class UserChoiceAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'choice_task')
