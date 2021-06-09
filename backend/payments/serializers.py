from rest_framework import serializers


class BillingDetailsSerializer(serializers.Serializer):
    name = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()
    address = serializers.CharField()
    postalCode = serializers.CharField()
    district = serializers.CharField(required=False)


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

