from ..base.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, JSONParser, FileUploadParser
from rest_framework.decorators import action
from rest_framework import response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema

from .serializers import AssignProjectSerializer, ProjectsSerializer, TasksSerializer, SubTasksSerializer
from .filters import ProjectFilter, AssignProjectFilter, TasksFilter, SubTasksFilter
from .models import Projects, Tasks, AssignProject, SubTasks
from ..base.services import create_update_record


class ProjectsViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    parser_classes = (JSONParser, MultiPartParser, FileUploadParser)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(ProjectsViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = ProjectFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @swagger_auto_schema(
        method="post",
        operation_summary='Create Tasks',
        operation_description='.',
        request_body=TasksSerializer,
        response=TasksSerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Tasks',
        operation_description='send id with data',
        request_body=TasksSerializer,
        response=TasksSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='Get Tasks',
        operation_description='',
        response=TasksSerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, serializer_class=TasksSerializer)
    def tasks(self, request):
        if request.user.is_authenticated:
            if request.method == "GET":
                queryset = Tasks.objects.filter(is_active=True)
                self.filterset_class = TasksFilter
                queryset = self.filter_queryset(queryset)
                return response.Response(TasksSerializer(queryset, many=True).data)
            else:
                return response.Response(create_update_record(request, TasksSerializer, Tasks))
        else:
            return response.Response({"detail": "User not authenticated."})

    @swagger_auto_schema(
        method="post",
        operation_summary='Create Sub Tasks',
        operation_description='.',
        request_body=SubTasksSerializer,
        response=SubTasksSerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Sub Tasks',
        operation_description='send id with data',
        request_body=SubTasksSerializer,
        response=SubTasksSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='Get Sub Tasks',
        operation_description='',
        response=SubTasksSerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False,  serializer_class=SubTasksSerializer)
    def sub_tasks(self, request):
        if request.user.is_authenticated:
            if request.method == "GET":
                queryset = SubTasks.objects.filter(is_active=True)
                self.filterset_class = SubTasksFilter
                queryset = self.filter_queryset(queryset)
                return response.Response(SubTasksSerializer(queryset, many=True).data)
            else:
                return response.Response(create_update_record(request, SubTasksSerializer, SubTasks))
        else:
            return response.Response({"detail": "User not authenticated."})

    @swagger_auto_schema(
        method="post",
        operation_summary='Assign Tasks',
        operation_description='.',
        request_body=AssignProjectSerializer,
        response=AssignProjectSerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Assignment',
        operation_description='send id with data',
        request_body=AssignProjectSerializer,
        response=AssignProjectSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='Get Assigned Tasks',
        operation_description='',
        response=AssignProjectSerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, serializer_class=AssignProjectSerializer)
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
                return response.Response(create_update_record(req_data, AssignProjectSerializer, AssignProject))
        else:
            return response.Response({"detail": "User not authenticated."})
