from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import CreateNewCompanySerializer, CreateCompanyOwnerProfile
from core.utils import IsSuperUser
from accounts.models import User
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_403_FORBIDDEN
from companys.models import Company, CompanyOwnerProfile

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

        temp_password = getattr(serializer, "generated_password", None)

        return Response(
            {
                "message":"Company Created Successfully",
                "slug":company.slug,
                "plan_active_till": company.plan_end_date,
                "company owner email": company.email,
                "temporary password":temp_password
            },
            status=HTTP_201_CREATED
        )
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@extend_schema(request=CreateCompanyOwnerProfile)
@api_view(['PUT', 'POST'])
@permission_classes([IsAuthenticated])
def edit_owner_profile(request, company_slug):
    try:
        OwnerProfile = request.user.company_owner_profile

        if OwnerProfile.company.slug != company_slug:
            return Response({"message":"You Are not Allowed To Edit Other Company Owner Data"}, status=HTTP_403_FORBIDDEN)
    except CompanyOwnerProfile.DoesNotExist:
        return Response({"detail": "Company owner proifle not found fot this disguise"}, status=HTTP_404_NOT_FOUND)


    serializer = CreateCompanyOwnerProfile(
        OwnerProfile, 
        data=request.data,
        partial = True
    )

    if serializer.is_valid():
        updated_profile = serializer.save()

        updated_profile.is_boarded = True
        updated_profile.save(update_fields=['is_boarded'])

        return Response({
            "message":"Details Edited / Added",
            "data":serializer.data
        },
            status=HTTP_200_OK
        )
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

     