from rest_framework import serializers
from projects.models import *
from django.db import transaction
from users.serializers import CustomUserSerializer
from decimal import *


class DataTypeTagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = DataTypeTag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class DataTagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    unit = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = DataTag
        fields = ('id', 'name', 'tag_type', 'unit')
        read_only_fields = ('id',)


class TaskListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(deleted=False)
        return super(TaskListSerializer, self).to_representation(data)


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    data_type_tag = DataTypeTagSerializer(required=False, allow_null=True)
    data_tags = DataTagSerializer(many=True)

    class Meta:
        list_serializer_class = TaskListSerializer
        model = Task
        fields = ('id', 'reward', 'deleted', 'batch', 'count',
                  'name', 'data_type_tag', 'data_tags', 'finished')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        data = super(TaskSerializer, self).to_representation(instance)
        data.update(
            {
                "reward": Decimal(instance.reward).normalize(),
                "batch": Decimal(instance.batch).normalize()
            }
        )
        return data


class MilestoneSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Milestone
        fields = ('id', 'name', 'tasks')


class ActionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    milestones = MilestoneSerializer(many=True)

    class Meta:
        model = Action
        fields = ('id', 'name', 'milestones')


class ProjectImageSerializer(serializers.Serializer):
    image = serializers.FileField()


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    description = serializers.CharField(required=False, allow_blank=True)

    image = serializers.FileField(read_only=True, required=False, allow_null=True)

    status = serializers.IntegerField(read_only=True)
    state = serializers.IntegerField(read_only=True)
    sync = serializers.IntegerField(read_only=True)

    start = serializers.DateField()
    end = serializers.DateField()

    actions = ActionSerializer(many=True)

    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'image',
            'status',
            'state',
            'sync',
            'start',
            'end',
            'actions',
            'fac_adm_funds',
            'created',
            'app_id'
        )

    def to_representation(self, instance):
        data = super(ProjectSerializer, self).to_representation(instance)
        data.update(
            {
                "fac_adm_funds": Decimal(instance.fac_adm_funds).normalize()
            }
        )
        return data

    def get_facilitator(self, obj):
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
        with transaction.atomic():
            project_obj = Project.objects.create(
                owner=self.context['owner'],
                title=validated_data['title'],
                description=validated_data['description'],
                start=validated_data['start'],
                end=validated_data['end'],
                fac_adm_funds=validated_data['fac_adm_funds']
            )

            for action in validated_data['actions']:
                action_obj = Action.objects.create(
                    project=project_obj,
                    name=action['name']
                )
                project_obj.actions.add(action_obj)

                for milestone in action['milestones']:
                    milestone_obj = Milestone.objects.create(
                        project=project_obj,
                        name=milestone['name'],
                    )
                    action_obj.milestones.add(milestone_obj)

                    for task in milestone['tasks']:
                        task_obj = Task.objects.create(
                            name=task['name'],
                            project=project_obj,
                            reward=task['reward'],
                            batch=task['batch'],
                            count=task['count']
                        )
                        milestone_obj.tasks.add(task_obj)

            project_obj.save()
            return project_obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            if (instance.fac_adm_funds != validated_data['fac_adm_funds'] or
                instance.start != validated_data['start'] or
                instance.end != validated_data['end']
            ):
                instance.sync = Project.TO_SYNC

            print("DDD", instance.fac_adm_funds != validated_data['fac_adm_funds'])
            instance.title = validated_data['title']
            instance.description = validated_data['description']
            instance.start = validated_data['start']
            instance.end = validated_data['end']
            instance.fac_adm_funds = validated_data['fac_adm_funds']

            actions_dict = {
                action.id: action for action in instance.actions.all()
            }
            for action in validated_data['actions']:
                if action.get('id', None):
                    action_obj = Action.objects.get(
                        id=action['id'],
                        project=instance
                    )
                    action_obj.name = action['name']
                    action_obj.save()
                    del actions_dict[action_obj.id]
                else:
                    action_obj = Action.objects.create(
                        project=instance,
                        name=action['name']
                    )
                    instance.actions.add(action_obj)

                milestones_dict = {
                    milestone.id: milestone for milestone in action_obj.milestones.all()
                }
                for milestone in action['milestones']:
                    if milestone.get('id', None):
                        milestone_obj = Milestone.objects.get(
                            id=milestone['id'],
                            project=instance
                        )
                        milestone_obj.name = milestone['name']
                        milestone_obj.save()
                        del milestones_dict[milestone_obj.id]
                    else:
                        milestone_obj = Milestone.objects.create(
                            project=instance,
                            name=action['name']
                        )
                        action_obj.milestones.add(milestone_obj)

                    tasks_dict = {
                        task.id: task for task in milestone_obj.tasks.all()
                    }
                    for task in milestone['tasks']:
                        if task.get('id', None):
                            task_obj = Task.objects.get(
                                id=task['id'],
                                project=instance,
                            )
                            task_obj.name = task['name']
                            task_obj.reward = task['reward']
                            task_obj.batch = task['batch']
                            task_obj.count = task['count']
                            del tasks_dict[task_obj.id]
                        else:
                            task_obj = Task.objects.create(
                                project=instance,
                                name=task['name'],
                                reward=task['reward'],
                                batch=task['batch'],
                                count=task['count']
                            )
                            milestone_obj.tasks.add(task_obj)

                        if task.get('data_type_tag', None):
                            dtt = task['data_type_tag']
                            dtt_obj = DataTypeTag.objects.get(
                                id=dtt['id']
                            )
                            task_obj.data_type_tag = dtt_obj
                        else:
                            task_obj.data_type_tag = None

                        task_obj.data_tags.clear()
                        for tag in task['data_tags']:
                            tag_obj = DataTag.objects.get(
                                id=tag['id']
                            )
                            task_obj.data_tags.add(tag_obj)
                        
                        task_obj.save()

            instance.save()
            return instance


class AssignmentSerializer(serializers.ModelSerializer):
    beneficiary = CustomUserSerializer(required=False, read_only=True)

    class Meta:
        model = Assignment
        fields = ('id', 'beneficiary', 'status', 'sync')
        read_only_fields = ('beneficiary', )
