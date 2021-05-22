from django.db import models
from django.contrib.auth import get_user_model

from ..base.models import TimeStampedModel
from ..base.services import file_extension_validator


class Projects(TimeStampedModel):
    name = models.CharField(blank=True, null=True, max_length=1024)
    description = models.TextField(blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Tasks(TimeStampedModel):
    project = models.ForeignKey(Projects, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(blank=True, null=True, max_length=1024)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class SubTasks(TimeStampedModel):
    task = models.ForeignKey(Tasks, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(blank=True, null=True, max_length=1024)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class AssignProject(TimeStampedModel):
    employees = models.ManyToManyField(get_user_model(), blank=True, related_name="employee")
    assigned_by = models.ForeignKey(get_user_model(), blank=True, null=True, related_name="assigned_by", on_delete=models.PROTECT)
    tasks = models.ManyToManyField(Tasks, blank=True)
    date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)



