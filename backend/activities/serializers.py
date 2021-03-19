from activities.models import Activity
from rest_framework import serializers
from projects.serializers import TaskSerializer


class ActivityProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class ActivitySerializer(serializers.ModelSerializer):
    project = ActivityProjectSerializer(required=False, read_only=True)
    task = TaskSerializer(required=False, read_only=True)

    class Meta:
        model = Activity
        fields = ('id', 'photo', 'task', 'project', 'task')
        read_only_fields = ('id', 'project', 'task')