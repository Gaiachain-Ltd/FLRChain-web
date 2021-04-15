from rest_framework import serializers
from projects.models import *
from django.db import transaction
from users.serializers import CustomUserSerializer
from investments.serializers import InvestmentSerializer


class TaskListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(deleted=False)
        return super(TaskListSerializer, self).to_representation(data)


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        list_serializer_class = TaskListSerializer
        model = Task
        fields = ('id', 'action', 'reward', 'deleted')
        read_only_fields = ('id',)


class ProjectSerializer(serializers.ModelSerializer):
    start = serializers.DateField()
    end = serializers.DateField()
    tasks = TaskSerializer(many=True)
    investment = InvestmentSerializer(required=False, read_only=True)
    assignment_status = serializers.IntegerField(required=False)
    facililator = serializers.SerializerMethodField(required=False, read_only=True)
    spent = serializers.DecimalField(max_digits=26, decimal_places=6, required=False, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'start', 'end',
                  'tasks', 'assignment_status', 'investment',
                  'facililator', 'spent')
        read_only_fields = ('assignment_status', 'investment',
                            'facililator', 'spent')

    def get_facililator(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}"

    def create(self, validated_data):
        with transaction.atomic():
            project = Project.objects.create(
                owner=self.context['owner'],
                title=validated_data['title'],
                description=validated_data['description'],
                start=validated_data['start'],
                end=validated_data['end'])

            for task in validated_data['tasks']:
                task_obj = Task.objects.create(
                    project=project,
                    action=task['action'],
                    reward=task['reward'])

                project.tasks.add(task_obj)

            project.save()
            return project

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.title = validated_data['title']
            instance.description = validated_data['description']
            instance.start = validated_data['start']
            instance.end = validated_data['end']

            tasks_dict = {task.id: task for task in instance.tasks.all()}
            for task in validated_data['tasks']:
                if task.get('id', None):
                    task_obj = Task.objects.get(
                        id=task['id'],
                        project=instance)
                    task_obj.action = task['action']
                    task_obj.reward = task['reward']
                    task_obj.save()
                    del tasks_dict[task_obj.id]
                else:
                    task_obj = Task.objects.create(
                        project=instance,
                        action=task['action'],
                        reward=task['reward'])
                    instance.tasks.add(task_obj)

            for task in tasks_dict.values():
                task.deleted = True
                task.save()

            instance.save()
            return instance


class AssignmentSerializer(serializers.ModelSerializer):
    beneficiary = CustomUserSerializer(required=False, read_only=True)

    class Meta:
        model = Assignment
        fields = ('id', 'beneficiary', 'status')
        read_only_fields = ('beneficiary', )