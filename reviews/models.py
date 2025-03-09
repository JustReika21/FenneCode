from django.contrib.auth import get_user_model
from django.db import models

from courses.models import Course


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    text = models.CharField(max_length=1024)
    rating = models.SmallIntegerField(
        default=0,
        choices=[(i, i) for i in range(1, 11)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        models.UniqueConstraint(fields=['user', 'course'], name='unique_review')

    def __str__(self):
        return f'{self.user} {self.course} ({self.rating}/10)'
