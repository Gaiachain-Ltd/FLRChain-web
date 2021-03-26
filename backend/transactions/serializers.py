from transactions.models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', required=False)
    
    class Meta:
        model = Transaction
        fields = ('id', 'txid', 'action', 'fee', 'modified',
                  'created', 'amount', 'project_name')