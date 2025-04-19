from django.contrib import admin

from courses.models import Course, Enrollment, CourseTag


@admin.register(CourseTag)
class CourseTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'progress', 'enrolled_at')
