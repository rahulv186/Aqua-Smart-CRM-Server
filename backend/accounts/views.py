from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..companys.models import Company

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request, company_slug):
    company = Company.objects.get(slug = company_slug)

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