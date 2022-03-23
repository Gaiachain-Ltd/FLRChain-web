from rest_framework import serializers
from decimal import *


class InvestmentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=26, decimal_places=6)