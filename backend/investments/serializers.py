from investments.models import Investment
from users.serializers import CustomUserSerializer
from rest_framework import serializers
from decimal import *


class InvestmentSerializer(serializers.ModelSerializer):
    investor = CustomUserSerializer(required=False, read_only=True)
    status = serializers.IntegerField(required=False)

    class Meta:
        model = Investment
        fields = ('id', 'investor', 'status', 'start',
                  'end', 'amount')
        read_only_fields = ('investor', 'status')

    def validate(self, data):
        if Decimal(data['amount']) < 0:
            raise serializers.ValidationError({"amount": "amount must be greater than zero"})
        
        if data['start'] > data['end']:
            raise serializers.ValidationError({"end": "end must occur after start"})

        return data