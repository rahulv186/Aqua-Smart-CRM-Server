from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Customer_RO_Purifier
from .serializers import CustomerROPurifierSerializer
from companys.models import Company
from core.utils import IsOwnerOrManager
from django.contrib.auth import get_user_model
User = get_user_model()



@extend_schema(responses={200: CustomerROPurifierSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsOwnerOrManager])
def purifier_list(request, company_slug):
    try:
        company = Company.objects.get(slug=company_slug)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    customer_id = request.query_params.get('customer_id')
    purifiers = Customer_RO_Purifier.objects.filter(company=company)
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
        serializer.save(company=company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@extend_schema(request=CustomerROPurifierSerializer, responses={200: CustomerROPurifierSerializer})
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def purifier_detail(request, company_slug, pk):
    try:
        company = Company.objects.get(slug=company_slug)
        purifier = Customer_RO_Purifier.objects.get(pk=pk)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
    except Customer_RO_Purifier.DoesNotExist:
        return Response({"error": "Purifier not found"}, status=status.HTTP_404_NOT_FOUND)

    if purifier.company != company:
        return Response({"error": "Resource does not belong to this company"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        serializer = CustomerROPurifierSerializer(purifier)
        return Response(serializer.data)

    if request.method == "PUT":
        # Ensure only Managers/Owners can update\
        if not (IsOwnerOrManager):
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CustomerROPurifierSerializer(purifier, data=request.data, context={'company': company}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from customers.models import CustomerUserProfile

@extend_schema(responses={200: CustomerROPurifierSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_purifier(request, company_slug):
    try:
        company = Company.objects.get(slug=company_slug)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get the customer profile specific to THIS company workspace
    try:
        customer_profile = CustomerUserProfile.objects.get(user=request.user, company=company)
    except CustomerUserProfile.DoesNotExist:
        return Response({"error": "Customer profile not found for this company"}, status=status.HTTP_404_NOT_FOUND)

    # Filter purifiers by both company and the correct workspace-specific profile
    purifiers = Customer_RO_Purifier.objects.filter(company=company, customer=customer_profile)
    
    serializer = CustomerROPurifierSerializer(purifiers, many=True)
    return Response(serializer.data)