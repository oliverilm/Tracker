from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255)
    has_ended = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField()
    stop = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    total_hours = models.CharField(max_length=10, blank=True, null=True)


class UserInProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
