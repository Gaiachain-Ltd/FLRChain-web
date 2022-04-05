from rest_framework import status
from rest_framework.response import Response
from users.models import Organization
from users.serializers import *
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from accounts.models import Account
from common.views import CommonView, NoGetQueryParametersSchema
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    url = f"{settings.FRONTEND_URL}/reset/?token={reset_password_token.key}"
    subject = "[FLRChain] Password reset"
    text_content = f"Please visit the following URL to reset your password:\n {url}"
    html_content = f'Please visit the following URL to reset your password:<br><a href="{url}">{url}</a>'
    msg = EmailMultiAlternatives(
        subject, 
        text_content, 
        settings.EMAIL_HOST_USER, 
        [reset_password_token.user.email,]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@swagger_auto_schema(
    operation_summary="Change password",
    method='POST',
    request_body=PasswordChangeSerializer,
    operation_description="Returns 'OK' string on success",
    responses={
        status.HTTP_200_OK: PasswordReplySerializer
    },
    tags=['users', 'facililator', 'beneficiary', 'investor']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = request.user

    if user.check_password(serializer.validated_data['old_password']):
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"status": "OK"}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    operation_summary="Register user",
    method='POST',
    request_body=UserSerializer,
    tags=['users', 'facililator', 'beneficiary', 'investor']
)
@api_view(['POST'])
@permission_classes([])
def user_register(request):
    with transaction.atomic():
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        Account.generate(user)

        return Response(status=status.HTTP_201_CREATED)
    

class CustomAuthToken(ObtainAuthToken):
    @swagger_auto_schema(
        operation_summary="Login user",
        operation_description=(
            "Beneficiary can log ONLY from mobile devices."
            "Facililators and investors ONLY from browsers."
        ),
        tags=['users', 'facililator', 'beneficiary', 'investor']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        is_qt_user_agent = request.META.get("HTTP_USER_AGENT", "") == "Qt"
        if ((is_qt_user_agent and user.type != CustomUser.BENEFICIARY) 
            or (not is_qt_user_agent and user.type == CustomUser.BENEFICIARY)
        ):
            raise serializers.ValidationError({'error': 'Incorrect browser.'})

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


class UserInfoView(CommonView):
    serializer_class= UserInfoSerializer

    @swagger_auto_schema(
        auto_schema=NoGetQueryParametersSchema,
        operation_summary="Get user profile",
        responses={
            status.HTTP_200_OK: UserInfoSerializer
        },
        tags=['users', 'facililator', 'beneficiary', 'investor']
    )
    def list(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update user profile",
        request_body=UserInfoSerializer,
        responses={
            status.HTTP_200_OK: UserInfoSerializer
        },
        tags=['users', 'facililator', 'beneficiary', 'investor']
    )
    def update(self, request):
        serializer = UserInfoSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganizationView(CommonView):
    serializer_class = OrganizationSerializer

    def list(self, request):
        organization, _ = Organization.objects.get_or_create(
            user=request.user
        )

        return Response(
            OrganizationSerializer(organization).data,
            status=status.HTTP_200_OK
        )

    def patrial_update(self, request, pk=None):
        organization, _ = Organization.objects.get_or_create(
            user=request.user
        )

        serializer = OrganizationSerializer(organization, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
