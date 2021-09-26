from django.db import models
from django.db.models import ForeignKey
from django.utils.timezone import now
from django.conf import settings


class Todo(models.Model):
    # no id field ?
    created = models.DateTimeField(default=now)
    title = models.CharField(max_length=200)
    description = models.TextField()
    done = models.BooleanField(default=False)
    priority = models.SmallIntegerField()
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Owner of todo tasks",
        on_delete=models.CASCADE,
        related_name='todos',
    )

    def __str__(self):
        return f'TODO task {self.id}; {self.title}'  # NOQA
