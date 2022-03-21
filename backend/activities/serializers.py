from activities.models import *
from rest_framework import serializers
from projects.serializers import TaskSerializer


class ActivityProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class ActivityBeneficiarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class ActivityPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('file',)


class ActivitySerializer(serializers.ModelSerializer):
    project = ActivityProjectSerializer(required=False, read_only=True)
    task = TaskSerializer(required=False, read_only=True)
    beneficiary = ActivityBeneficiarySerializer(source="user", read_only=True)
    txid = serializers.CharField(source="transaction.txid", required=False)
    photos = ActivityPhotoSerializer(read_only=True, many=True)
    text = serializers.CharField(required=False)
    area = serializers.IntegerField(required=False)
    number = serializers.IntegerField(required=False)

    class Meta:
        model = Activity
        fields = ('id', 'project', 'task',
                  'created', 'beneficiary', 'txid', 'sync',
                  'photos', 'text', 'area', 'number')
        read_only_fields = ('id', 'project', 'task', 'beneficiary',
                            'txid', 'sync')


class ActivityVerificationSerializer(serializers.Serializer):
    status = serializers.IntegerField()