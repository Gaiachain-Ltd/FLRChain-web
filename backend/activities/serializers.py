from activities.models import Activity
from rest_framework import serializers
from projects.serializers import TaskSerializer


class ActivityProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class ActivityBeneficiarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class ActivitySerializer(serializers.ModelSerializer):
    project = ActivityProjectSerializer(required=False, read_only=True)
    task = TaskSerializer(required=False, read_only=True)
    beneficiary = ActivityBeneficiarySerializer(source="user", read_only=True)
    txid = serializers.CharField(source="transaction.txid", required=False)

    class Meta:
        model = Activity
        fields = ('id', 'photo', 'task', 'project', 'task',
                  'created', 'beneficiary', 'txid')
        read_only_fields = ('id', 'project', 'task', 'beneficiary',
                            'txid')


class ActivityVerificationSerializer(serializers.Serializer):
    status = serializers.IntegerField()