from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from hr.serializers import CreateHRProfile
from core.utils import IsOwnerOrManagerOrHR
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
)
from companys.models import Company
from django.contrib.auth import get_user_model

User = get_user_model()


@extend_schema(
    request=CreateHRProfile,
    responses={201: {"description": "Invitation sent successfully."}}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsOwnerOrManagerOrHR])
def create_hr(request, company_slug):
    try:
        company = Company.objects.get(slug=company_slug)

    except Company.DoesNotExist:
        return Response(
            {"error": "Company not found."}, 
            status=HTTP_404_NOT_FOUND
        )
    serializer = CreateHRProfile(data=request.data)

    if serializer.is_valid():
        user, password, technician_profile = serializer.save(company=company)
        return Response({
            "message":"Technician User and Profile are Generated and Filled",
            "user":{
                "email":user.email,
                "password":password
            },
            "profile":{
                "name":technician_profile.name,
                "employee_code":technician_profile.employee_code,
                "is_active":technician_profile.is_active
            }
        },
        status=HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

