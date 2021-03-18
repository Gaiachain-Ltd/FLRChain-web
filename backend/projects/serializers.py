from rest_framework import serializers
from projects.models import *
from django.db import transaction
from users.serializers import CustomUserSerializer


class InvestmentSerializer(serializers.ModelSerializer):
    investor = CustomUserSerializer(required=False, read_only=True)
    status = serializers.IntegerField(required=False)
    start = serializers.DateField()
    end = serializers.DateField()
    amount = serializers.IntegerField()

    class Meta:
        model = Investment
        fields = ('id', 'investor', 'status', 'start',
                  'end', 'amount')
        read_only_fields = ('investor', 'status')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'action', 'reward')


class ProjectSerializer(serializers.ModelSerializer):
    start = serializers.DateField()
    end = serializers.DateField()
    tasks = TaskSerializer(many=True)
    investment = InvestmentSerializer(required=False, read_only=True)
    assignment_status = serializers.IntegerField(required=False)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'start', 'end',
                  'tasks', 'assignment_status', 'investment')
        read_only_fields = ('assignment_status', 'investment')

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


class AssignmentSerializer(serializers.ModelSerializer):
    beneficiary = CustomUserSerializer(required=False, read_only=True)

    class Meta:
        model = Assignment
        fields = ('id', 'beneficiary', 'status')
        read_only_fields = ('beneficiary', )