from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import RegisterSerializer, SuperUserTokenObtainPairSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from companys.models import Company
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

# Create your views here.
from rest_framework import serializers  # Make sure this is imported
from drf_spectacular.utils import extend_schema, inline_serializer

@extend_schema(
    responses={
        200: inline_serializer(
            name="UserMeResponse",  # Name shown in Swagger docs
            fields={
                "email": serializers.EmailField(),
                "username": serializers.CharField(),
                "role": serializers.CharField(),
                # Add any other keys that your /me view returns in its dictionary
            }
        )
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request, company_slug):

    return Response({
        "email": request.user.email,
        "username": request.user.username,
    })



@extend_schema(request=RegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request, company_slug):
    try:
        company = Company.objects.get(slug = company_slug)
    except Company.DoesNotExist:
        return Response(
            {"error": f"Company workspace '{company_slug}' not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )

    if(not company):
        return Response({"message":"Company Does Not Exist"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RegisterSerializer(data = request.data)
    if(serializer.is_valid()):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message":"Created Successfully",
                "user":{
                    "id": str(user.id),
                    "full_name":user.full_name,
                    "email":user.email,
                    "phone":user.phone,
                    "password":user.password,
                    "company":company
                },
                "tokens":{
                    "refresh_token":str(refresh),
                    "access_token":str(refresh.access_token)
                }

            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



@extend_schema(request=SuperUserTokenObtainPairSerializer)
class SuperUserTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = SuperUserTokenObtainPairSerializer