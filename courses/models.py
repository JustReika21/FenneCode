from django.db import models

from fennecode import settings


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skill_requirements = models.TextField()
    duration = models.SmallIntegerField()
    # TODO: rating
    # rating = DecimalField?
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authors'
    )
    slug = models.SlugField(unique=True)
    cover = models.ImageField(
        upload_to="courses_covers/",
        default='courses_covers/default.jpg'
    )
    total_points = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    points = models.IntegerField(default=0)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'user'],
                name='unique_enrollment'
            )
        ]
