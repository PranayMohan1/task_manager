import django_filters

from .models import Projects, AssignProject, Tasks, SubTasks


class ProjectFilter(django_filters.FilterSet):

    class Meta:
        model = Projects
        fields = {
            'id': ['exact'],
            'name': ['icontains']
        }


class TasksFilter(django_filters.FilterSet):
    class Meta:
        model = Tasks
        fields = {
            'id': ['exact'],
            'name': ['icontains'],
            'project': ['exact']
        }


class SubTasksFilter(django_filters.FilterSet):
    class Meta:
        model = SubTasks
        fields = {
            'id': ['exact'],
            'name': ['icontains'],
            'task': ['exact']
        }


class AssignProjectFilter(django_filters.FilterSet):
    class Meta:
        model = AssignProject
        fields = {
            'id': ['exact'],
            'employees': ['exact'],
            'tasks': ['exact'],
            'assigned_by': ['exact']
        }