from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'password', 'email', 'type')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            validated_data['email'],
            validated_data['password'],
            type=validated_data.get('type', CustomUser.BENEFICIARY))

        return user
