from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import CreateNewCompanySerializer
from accounts.permissions import IsSuperUser
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

# Create your views here.
@extend_schema(request=CreateNewCompanySerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsSuperUser])
def createCompany(request):
    serializer = CreateNewCompanySerializer

    serializer = CreateNewCompanySerializer(
        data = request.data
    )

    if serializer.is_valid():
        company = serializer.save()

        return Response(
            {
                "message":"Company Created Successfully",
                "slug":company.slug,
                "plan_active_till": company.plan_end_date
            },
            status=HTTP_201_CREATED

        )
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)