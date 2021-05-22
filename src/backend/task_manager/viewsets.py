from ..base.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, JSONParser, FileUploadParser
from rest_framework.decorators import action
from rest_framework import response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .serializers import AssignProjectSerializer, ProjectsSerializer, TasksSerializer, SubTasksSerializer
from .filters import ProjectFilter, AssignProjectFilter, TasksFilter, SubTasksFilter
from .models import Projects, Tasks, AssignProject, SubTasks
from ..base.services import create_update_record

import base64
import json

from django.core.files.base import ContentFile


class ProjectsViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    parser_classes = (JSONParser, MultiPartParser, FileUploadParser)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def perform_create(self, serializer):
        if self.request:
            """print(self.request.data)
            data = self.request.data.copy()
            img_format, imgstr = data['avatar'].split(';base64,')
            ext = img_format.split('/')[-1]
            data['avatar'] = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)"""
        serializer.save()

    def perform_update(self, serializer):
        action_by = None
        if self.request and hasattr(self.request, "user"):
            action_by = self.request.user
        serializer.save(action_by=action_by)

    def get_queryset(self):
        queryset = super(ProjectsViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = ProjectFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @action(methods=['GET', 'POST', 'PUT'], detail=False)
    def tasks(self, request):
        if request.user.is_authenticated:
            if request.method == "GET":
                queryset = Tasks.objects.filter(is_active=True)
                self.filterset_class = TasksFilter
                queryset = self.filter_queryset(queryset)
                return response.Response(TasksSerializer(queryset, many=True).data)
            else:
                return create_update_record(request, TasksSerializer, Tasks)
        else:
            return response.Response({"detail": "User not authenticated."})

    @action(methods=['GET', 'POST', 'PUT'], detail=False)
    def sub_tasks(self, request):
        if request.user.is_authenticated:
            if request.method == "GET":
                queryset = SubTasks.objects.filter(is_active=True)
                self.filterset_class = SubTasksFilter
                queryset = self.filter_queryset(queryset)
                return response.Response(SubTasksSerializer(queryset, many=True).data)
            else:
                return create_update_record(request, SubTasksSerializer, SubTasks)
        else:
            return response.Response({"detail": "User not authenticated."})

    @action(methods=['GET', 'POST', 'PUT'], detail=False)
    def assign_tasks(self, request):
        if request.user.is_authenticated:
            if request.method == "GET":
                queryset = AssignProject.objects.filter(is_active=True)
                self.filterset_class = AssignProjectFilter
                queryset = self.filter_queryset(queryset)
                return response.Response(AssignProjectSerializer(queryset, many=True).data)
            else:
                req_data = request.data.copy()
                req_data["assigned_by"] = self.request.user.pk
                req_data["date"] = (timezone.localtime(timezone.now())).date()
                return create_update_record(request, AssignProjectSerializer, AssignProject)
        else:
            return response.Response({"detail": "User not authenticated."})
