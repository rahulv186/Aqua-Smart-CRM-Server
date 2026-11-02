from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from .models import Customer_RO_Purifier
from .serializers import CustomerROPurifierSerializer
from companys.models import Company
from customers.models import CustomerUserProfile
from core.utils import IsOwnerOrManager
from django.contrib.auth import get_user_model

User = get_user_model()


@extend_schema(responses={200: CustomerROPurifierSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsOwnerOrManager])
def purifier_list(request, company_slug):
    try:
        company = Company.objects.get(slug=company_slug)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    purifiers = Customer_RO_Purifier.objects.filter(company=company)
    
    # Optional filters: by status (e.g., ?status=in_warehouse) or customer_id
    purifier_status = request.query_params.get('status')
    if purifier_status:
        purifiers = purifiers.filter(status=purifier_status)

    customer_id = request.query_params.get('customer_id')
    if customer_id:
        purifiers = purifiers.filter(customer_id=customer_id)

    serializer = CustomerROPurifierSerializer(purifiers, many=True)
    return Response(serializer.data)


@extend_schema(request=CustomerROPurifierSerializer, responses={201: CustomerROPurifierSerializer})
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsOwnerOrManager])
def purifier_create(request, company_slug):
    try:
        company = Company.objects.get(slug=company_slug)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerROPurifierSerializer(data=request.data, context={'company': company})
    if serializer.is_valid():
        # New units register in the warehouse by default
        serializer.save(company=company, status=Customer_RO_Purifier.PurifierStatus.IN_WAREHOUSE)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=CustomerROPurifierSerializer, responses={200: CustomerROPurifierSerializer})
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated, IsOwnerOrManager])
def purifier_detail(request, company_slug, pk):
    try:
        company = Company.objects.get(slug=company_slug)
        purifier = Customer_RO_Purifier.objects.get(pk=pk, company=company)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
    except Customer_RO_Purifier.DoesNotExist:
        return Response({"error": "Purifier not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CustomerROPurifierSerializer(purifier)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = CustomerROPurifierSerializer(purifier, data=request.data, context={'company': company}, partial=True)
        if serializer.is_valid():
            updated_purifier = serializer.save()
            
            # If a customer was assigned during this update and it was in the warehouse, trigger installation FSM transition
            if updated_purifier.customer and updated_purifier.status == Customer_RO_Purifier.PurifierStatus.IN_WAREHOUSE:
                if hasattr(updated_purifier, 'install_unit'):
                    updated_purifier.install_unit(
                        customer_profile=updated_purifier.customer, 
                        install_date=timezone.now().date()
                    )
                    updated_purifier.save()

            return Response(CustomerROPurifierSerializer(updated_purifier).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses={200: CustomerROPurifierSerializer})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def purifier_lookup_by_serial(request, company_slug):
    try:
        company = Company.objects.get(slug=company_slug)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    serial = request.query_params.get('serial')
    if not serial:
        return Response({"error": "Serial number parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        purifier = Customer_RO_Purifier.objects.get(company=company, serial_number=serial)
    except Customer_RO_Purifier.DoesNotExist:
        return Response({"error": "Purifier not found for this serial number"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerROPurifierSerializer(purifier)
    return Response(serializer.data)


@extend_schema(responses={200: CustomerROPurifierSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_purifier(request, company_slug):
    try:
        company = Company.objects.get(slug=company_slug)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        customer_profile = CustomerUserProfile.objects.get(user=request.user, company=company)
    except CustomerUserProfile.DoesNotExist:
        return Response({"error": "Customer profile not found for this company"}, status=status.HTTP_404_NOT_FOUND)

    purifiers = Customer_RO_Purifier.objects.filter(company=company, customer=customer_profile)
    
    serializer = CustomerROPurifierSerializer(purifiers, many=True)
    return Response(serializer.data)