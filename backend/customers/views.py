from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterNewCustomerSerializer
from companys.models import Company
from accounts.models import User
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from drf_spectacular.utils import extend_schema

# Create your views here.

@extend_schema(request=RegisterNewCustomerSerializer)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register(request, CompanySlug):
    serializer = RegisterNewCustomerSerializer
    user = request.user
    company = Company.objects.get(slug=CompanySlug)

    if hasattr(user, "customer_user_profile") and user.customer_user_profile.exists():
        return Response({"error": "Profile Already Exists"})

    serializer = RegisterNewCustomerSerializer(
        data=request.data, context={"user": user, "company": company}
    )

    if serializer.is_valid():
        profile = serializer.save()

        return Response(
            {
                "message": "Profile Created Successfully",
                "customer_code":profile.customer_code,
                "name":profile.name
             }, 
             status=HTTP_201_CREATED
        )
    else:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
