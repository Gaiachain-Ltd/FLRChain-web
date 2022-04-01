from transactions.models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.Serializer):
    id = serializers.CharField()
    amount = serializers.CharField()
    action = serializers.ChoiceField(choices=(
            (1, "Received"), 
            (2, "Sent")
        )
    )
    created = serializers.DateTimeField()
    project_id = serializers.IntegerField(required=False)
    project_name = serializers.CharField(required=False)