from investments.models import Investment
from users.serializers import CustomUserSerializer
from rest_framework import serializers


class InvestmentSerializer(serializers.ModelSerializer):
    investor = CustomUserSerializer(required=False, read_only=True)
    status = serializers.IntegerField(required=False)
    start = serializers.DateField()
    end = serializers.DateField()
    amount = serializers.IntegerField()

    class Meta:
        model = Investment
        fields = ('id', 'investor', 'status', 'start',
                  'end', 'amount')
        read_only_fields = ('investor', 'status')