from transactions.models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    project_name = serializers.CharField(source='project.title', required=False)
    
    class Meta:
        model = Transaction
        fields = ('id', 'txid', 'action', 'created', 'amount', 
                  'project_name', 'status')