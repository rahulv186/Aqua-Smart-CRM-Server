from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

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
def register(request):
    serializer = RegisterSerializer(data = request.data)
    if(serializer.is_valid()):
        refresh = RefreshToken.for_user(user)
        user = serializer.save
        return Response(
            {
                "message":"Created Successfully",
                "user":{
                    "id": str(user.id),
                    "full_name":user.full_name,
                    "email":user.email,
                    "phone":user.phone,
                    "password hash":user.passwordhash
                },
                "tokens":{
                    "refresh":refresh,
                    "access":refresh.access_token
                }

            },
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)