from rest_framework import serializers


class BillingDetailsSerializer(serializers.Serializer):
    name = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()
    line1 = serializers.CharField()
    line2 = serializers.CharField(required=False)
    district = serializers.CharField(required=False)
    postalCode = serializers.CharField()


class SaveCardSerializer(serializers.Serializer):
    idempotencyKey = serializers.CharField()
    keyId = serializers.CharField()
    email = serializers.EmailField()
    phoneNumber = serializers.CharField(required=False)
    expiry = serializers.CharField()
    encryptedData = serializers.CharField()
    billingDetails = BillingDetailsSerializer()

class MakePaymentSerializer(serializers.Serializer):
    idempotencyKey = serializers.CharField()
    keyId = serializers.CharField()
    amount = serializers.DecimalField(max_digits=26, decimal_places=6)
    cardId = serializers.CharField()
    encryptedData = serializers.CharField()

