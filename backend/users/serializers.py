from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'password', 'email', 'type',
                  'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            validated_data['email'],
            validated_data['password'],
            type=validated_data.get('type', CustomUser.BENEFICIARY),
            first_name=validated_data.get('first_name', ""),
            last_name=validated_data.get('last_name', ""))

        return user
