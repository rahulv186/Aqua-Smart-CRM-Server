from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from companys.serializers import SendInviteSerializer
from core.utils import IsOwnerOfCompany, IsManager
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
from invitation.models import Invitation


@extend_schema(
    request=SendInviteSerializer,
    responses={201: {"description": "Invitation sent successfully."}}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsOwnerOfCompany, IsManager])
def send_technician_invite(request, company_slug):

    try:
        company = Company.objects.get(slug=company_slug)

        if not company:
            return Response({"message": "Permission Denied"}, status=HTTP_403_FORBIDDEN)
    except Company.DoesNotExist:
        return Response(
            {"message": "Company Does Not Exist"}, status=HTTP_400_BAD_REQUEST
        )

    email = request.data.get("email")
    if not email:
        return Response({"error": "Email is Required"}, status=HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "User already Exists with same Email"},
            status=HTTP_400_BAD_REQUEST,
        )

    invitation = Invitation.objects.create(email=email, company=company, role="technician")

    invitation_link = f"http://app.aquasmart.ai/accept-invite?token={invitation.token}"

    # Email Service Link here
    
    return Response(
        {"message": "Invite link created", "link": invitation_link},
        status=HTTP_201_CREATED,
    )
