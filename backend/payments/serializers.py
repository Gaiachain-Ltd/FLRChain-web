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
    keyId = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    expiry = serializers.CharField()
    encryptedData = serializers.CharField()
    billingDetails = BillingDetailsSerializer()

