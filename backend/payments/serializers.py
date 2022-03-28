from rest_framework import serializers
from projects.models import Project


class BillingDetailsSerializer(serializers.Serializer):
    name = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()
    address = serializers.CharField()
    postalCode = serializers.CharField()
    district = serializers.CharField(required=False, allow_blank=True)


class SaveCardSerializer(serializers.Serializer):
    idempotencyKey = serializers.CharField()
    keyId = serializers.CharField()
    expiry = serializers.CharField()
    encryptedData = serializers.CharField()
    billingDetails = BillingDetailsSerializer()


class MakePaymentSerializer(serializers.Serializer):
    idempotencyKey = serializers.CharField()
    keyId = serializers.CharField()
    amount = serializers.DecimalField(max_digits=26, decimal_places=6)
    cardId = serializers.CharField()
    encryptedData = serializers.CharField()


class MTNPayoutSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=26, decimal_places=6)
    phone = serializers.CharField()


class FacililatorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="owner.id")
    first_name = serializers.CharField(source="owner.first_name")
    last_name = serializers.CharField(source="owner.last_name")

    class Meta:
        model = Project
        fields = ('id', 'first_name', 'last_name')


class FacililatorPayoutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=26, decimal_places=6)


class PayoutResultSerializer(serializers.Serializer):
    txid = serializers.CharField(required=False)
    success = serializers.BooleanField()