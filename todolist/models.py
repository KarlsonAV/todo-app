from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Task(models.Model):

    title = models.CharField(max_length=150, null=False)
    body = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):

        return self.title

    def get_absolute_url(self):

        return reverse('task_list', )
