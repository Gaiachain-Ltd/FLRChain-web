from rest_framework import serializers
from projects.models import *
from django.db import transaction
from users.serializers import CustomUserSerializer
from investments.serializers import InvestmentSerializer
from decimal import *
import datetime


class TaskListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(deleted=False)
        return super(TaskListSerializer, self).to_representation(data)


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        list_serializer_class = TaskListSerializer
        model = Task
        fields = ('id', 'reward', 'deleted', 'batch', 'count',
                  'name')
        read_only_fields = ('id',)

    def validate(self, data):
        if Decimal(data['reward']) < 0:
            raise serializers.ValidationError(
                {"reward": "reward must be greater than zero"})
        return data


class MilestoneSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Milestone
        fields = ('id', 'name', 'tasks')


class ProjectSerializer(serializers.ModelSerializer):
    start = serializers.DateField()
    end = serializers.DateField()
    investment = InvestmentSerializer(required=False, read_only=True)
    assignment_status = serializers.IntegerField(required=False)
    facililator = serializers.SerializerMethodField(
        required=False, read_only=True)
    spent = serializers.DecimalField(
        max_digits=26, decimal_places=6, required=False, read_only=True)
    status = serializers.IntegerField(required=False)
    milestones = MilestoneSerializer(many=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'start', 'end',
                  'assignment_status', 'investment',
                  'facililator', 'spent', 'status', 'milestones',
                  'fundraising_duration', 'fac_adm_funds')
        read_only_fields = ('assignment_status', 'investment',
                            'facililator', 'spent', 'status')

    def get_facililator(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}"

    def validate(self, data):
        """
        Check that the start is before the end.
        """
        if data['start'] > data['end']:
            raise serializers.ValidationError(
                {"end": "end must occur after start"})
        return data

    def create(self, validated_data):
        now = datetime.datetime.now()
        start_dt = datetime.datetime.combine(
            validated_data['start'], now.time())
        fundraising_start_dt = start_dt - \
            datetime.timedelta(days=validated_data['fundraising_duration'])

        if now.date() < fundraising_start_dt.date():
            raise serializers.ValidationError(
                {
                    "start": "incorrect start date",
                    "fundraising_duration": "incorrect fundraising duration"
                })

        with transaction.atomic():
            project_obj = Project.objects.create(
                owner=self.context['owner'],
                title=validated_data['title'],
                description=validated_data['description'],
                start=validated_data['start'],
                end=validated_data['end'],
                fundraising_duration=validated_data['fundraising_duration'],
                fac_adm_funds=validated_data['fac_adm_funds']
            )

            for milestone in validated_data['milestones']:
                milestone_obj = Milestone.objects.create(
                    project=project_obj,
                    name=milestone['name'],
                )
                project_obj.milestones.add(milestone_obj)
                
                for task in milestone['tasks']:
                    task_obj = Task.objects.create(
                        project=project_obj,
                        milestone=milestone_obj,
                        reward=task['reward'],
                        batch=task['batch'],
                        count=task['count']
                    )
                    milestone_obj.tasks.add(task_obj)

            project_obj.save()
            return project_obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.title = validated_data['title']
            instance.description = validated_data['description']
            instance.start = validated_data['start']
            instance.end = validated_data['end']

            tasks_dict = {
                task.id: task for task in instance.tasks.filter(deleted=False)}
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
