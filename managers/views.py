from django.shortcuts import render
from managers.serializers import (
    AcceptManagerInviteSerializer,
    ManagerProfileOnboardSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from companys.models import Company
from core.utils import IsManager
from drf_spectacular.utils import extend_schema
from invitation.models import Invitation

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_invite_link(request):

    token = request.query_params.get("token")

    if not token:
        return Response(
            {"error": "Token query parameter is required."}, 
            status=HTTP_400_BAD_REQUEST
        )

    try:
        invitation = Invitation.objects.get(token=token)

    except Invitation.DoesNotExist:
        return Response(
            {"error": "Invalid invitation token."}, 
            status=HTTP_404_NOT_FOUND
        )

    
    if not invitation.is_valid():
        return Response(
            {"error": "This invitation has expired or has already been used."}, 
            status=HTTP_400_BAD_REQUEST
        )

    return Response({
        "message":"Invite Link is verified and Legit",
        "email":invitation.email,
        "company":invitation.company
    }, status=HTTP_200_OK)






# Phase 1
@extend_schema(request=AcceptManagerInviteSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
def accept_manager_invite(request, company_slug):
    serializer = AcceptManagerInviteSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Account Created and Manager Profile Setup Done",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=HTTP_201_CREATED,
        )

    else:
        return Response(serializer.error_messages, status=HTTP_400_BAD_REQUEST)



# Phase 2
@extend_schema(request=ManagerProfileOnboardSerializer)
@api_view(["PATCH", "PUT"])
@permission_classes([IsAuthenticated, IsManager])
def manager_onboarding(request, company_slug):
    try:
        profile = request.user.manager_profile.first()
        company = Company.objects.get(slug=company_slug)
        if (not profile.company == company) or (not profile):
            return Response(
                {"error": "Permission Denied"}, status=HTTP_401_UNAUTHORIZED
            )

    except Company.DoesNotExist:
        return Response(
            {"error": "Company with the slug does not exist"},
            status=HTTP_400_BAD_REQUEST,
        )

    serializer = ManagerProfileOnboardSerializer(
        profile, data=request.data, partial=True
    )

    if serializer.is_valid():
        updated_profile = serializer.save()
        updated_profile.is_boarded = True
        updated_profile.save(update_fields=["is_boarded"])

        return Response(
            {"message": "Onboarding Successfull", "data": serializer.data},
            status=HTTP_200_OK,
        )
    else:
        return Response(serializer.error_messages, status=HTTP_400_BAD_REQUEST)


