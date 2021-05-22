from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Projects, Tasks, SubTasks, AssignProject
from ..accounts.serializers import UserSerializer


class ProjectsSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


class SubTasksDataSerializer(ModelSerializer):
    class Meta:
        model = SubTasks
        fields = '__all__'


class TasksSerializer(ModelSerializer):
    project_data = serializers.SerializerMethodField(required=False)
    sub_tasks_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Tasks
        fields = '__all__'

    def validate(self, data):
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"detail": "Start date can't be after end date."})
        return data

    @staticmethod
    def get_project_data(obj):
        return ProjectsSerializer(obj.project).data if obj.project else None

    @staticmethod
    def get_sub_tasks_data(obj):
        return SubTasksDataSerializer(SubTasks.objects.filter(task=obj, is_active=True), many=True).data


class SubTasksSerializer(ModelSerializer):
    task_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = SubTasks
        fields = '__all__'

    def validate(self, data):
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({"detail": "Start date can't be after end date."})
        return data


    @staticmethod
    def get_task_data(obj):
        return TasksSerializer(obj.task).data if obj.task else None


class AssignProjectSerializer(ModelSerializer):
    employees_data = serializers.SerializerMethodField(required=False)
    tasks_data = serializers.SerializerMethodField(required=False)
    assigned_by_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = AssignProject
        fields = '__all__'

    def validate(self, data):
        tasks = data.get("tasks", [])
        if AssignProject.objects.filter(tasks__in=tasks, is_active=True).exists():
            raise serializers.ValidationError({"detail": "Task already assigned"})
        return data

    @staticmethod
    def get_employees_data(obj):
        return UserSerializer(obj.employees.all(), many=True).data if obj.employees else None

    @staticmethod
    def get_tasks_data(obj):
        return TasksSerializer(obj.tasks.all(), many=True).data if obj.tasks else None

    @staticmethod
    def get_assigned_by_data(obj):
        return UserSerializer(obj.assigned_by).data if obj.assigned_by else None


