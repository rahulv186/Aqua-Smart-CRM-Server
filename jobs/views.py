from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from companys.models import Company
from customers.models import CustomerUserProfile
from core.utils import IsOwnerOrManager
from jobs.serializers import CreateServiceTicketForStaffSerializer, CreateServiceTicketForCustomerSerializer
from drf_spectacular.utils import extend_schema

# --- Staff / Manager Ticket Creation ---
@extend_schema(request=CreateServiceTicketForStaffSerializer, responses={201: CreateServiceTicketForStaffSerializer})
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsOwnerOrManager])  # Enforce staff/manager permissions
def create_ticket_staff(request, company_slug):
    try:
        company = Company.objects.get(slug=company_slug)
    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

    # Pass company and request in serializer context
    serializer = CreateServiceTicketForStaffSerializer(
        data=request.data, 
        context={'company': company, 'request': request}
    )
    
    if serializer.is_valid():
        ticket = serializer.save()
        return Response({"message": "Service ticket created successfully.", "ticket_id": str(ticket.id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Customer Ticket Creation ---
@extend_schema(request=CreateServiceTicketForCustomerSerializer, responses={201: CreateServiceTicketForCustomerSerializer})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_ticket(request, company_slug):
    try:
        company = Company.objects.get(slug=company_slug)
    except Company.DoesNotExist:
        return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

    # Verify the customer actually has a profile for THIS company workspace
    try:
        CustomerUserProfile.objects.get(user=request.user, company=company)
    except CustomerUserProfile.DoesNotExist:
        return Response({"error": "Customer profile not found for this company workspace."}, status=status.HTTP_403_FORBIDDEN)

    # Pass company and request in serializer context
    serializer = CreateServiceTicketForCustomerSerializer(
        data=request.data, 
        context={'company': company, 'request': request}
    )
    
    if serializer.is_valid():
        ticket = serializer.save()
        return Response({"message": "Service ticket created successfully.", "ticket_id": str(ticket.id)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

