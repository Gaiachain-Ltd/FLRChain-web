from activities.models import *
from rest_framework import serializers


class ActivityProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class ActivityTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

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
    task = ActivityTaskSerializer(required=False, read_only=True)
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

class CreateActivitySerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=False)
    area = serializers.IntegerField(required=False)
    number = serializers.IntegerField(required=False)

    class Meta:
        model = Activity
        fields = ('text', 'area', 'number')

class ActivityVerificationSerializer(serializers.Serializer):
    status = serializers.IntegerField()