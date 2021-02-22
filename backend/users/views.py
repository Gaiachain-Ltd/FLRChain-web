from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.serializers import CustomUserSerializer

class CustomUserView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)