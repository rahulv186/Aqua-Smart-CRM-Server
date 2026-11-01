from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterNewCustomerSerializer
from companys.models import Company
from customers.models import CustomerUserProfile
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from drf_spectacular.utils import extend_schema

User = get_user_model()

@extend_schema(request=RegisterNewCustomerSerializer)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register(request, company_slug):
    user = request.user
    
    try:
        company = Company.objects.get(slug=company_slug)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=HTTP_400_BAD_REQUEST)

    # ✅ Query the model directly to see if a profile already exists for this user in this company
    if CustomerUserProfile.objects.filter(user=user, company=company).exists():
        return Response({"error": "Profile Already Exists for this company"}, status=HTTP_400_BAD_REQUEST)

    serializer = RegisterNewCustomerSerializer(
        data=request.data, context={"user": user, "company": company}
    )

    if serializer.is_valid():
        profile = serializer.save()
        return Response(
            {
                "message": "Profile Created Successfully",
                "customer_code": profile.customer_code,
                "name": profile.name
            }, 
            status=HTTP_201_CREATED
        )
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)