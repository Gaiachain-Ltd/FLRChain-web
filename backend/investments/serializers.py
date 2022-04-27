from rest_framework import serializers


class InvestmentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=26, decimal_places=6)