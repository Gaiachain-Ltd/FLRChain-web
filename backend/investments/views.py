from django.shortcuts import  get_object_or_404
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from investments.serializers import InvestmentSerializer
from common.views import CommonView
from projects.models import Project
from investments.models import Investment
from rest_framework.response import Response


class InvestmentView(CommonView):
    serializer_class = InvestmentSerializer

    @swagger_auto_schema(
        operation_summary="Invest in project",
        request_body=InvestmentSerializer,
        tags=['investor'])
    def create(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        start = serializer.validated_data['start']
        end = serializer.validated_data['end']

        project = get_object_or_404(
            Project, 
            pk=pk, 
            investment=None,
            start__lte=start,
            end__gte=end)

        investment = Investment.objects.create(
            project=project,
            investor=request.user,
            amount=serializer.validated_data['amount'],
            start=start,
            end=end)

        serializer = self.serializer_class(investment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        operation_summary="Investment details",
        tags=['investor'])
    def retrieve(self, request, pk=None):
        project = get_object_or_404(
            Project, 
            pk=pk, 
            investment__isnull=False)

        investment = project.investment
        serializer = self.serializer_class(investment)
        return Response(serializer.data, status=status.HTTP_200_OK)