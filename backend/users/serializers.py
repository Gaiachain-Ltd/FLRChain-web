from rest_framework import serializers
from users.models import CustomUser, Organization


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False, allow_blank=True)
    village = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'password', 'email', 'type',
                  'first_name', 'last_name', 'phone',
                  'village',)
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
            last_name=validated_data.get('last_name', ""),
            phone=validated_data.get('phone', ""),
            village=validated_data.get('village', ""))

        return user


class UserInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False, allow_blank=True)
    village = serializers.CharField(required=False, allow_blank=True)
    opted_in = serializers.SerializerMethodField(read_only=True)
    type = serializers.ChoiceField(choices=CustomUser.USER_TYPES)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'type', 'first_name', 'last_name', 
                  'phone', 'village', 'opted_in')

    def get_opted_in(self, obj):
        return obj.opted_in


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'organization_type', 'website',
                  'statement', 'principal', 'email', 'phone')
