from django.shortcuts import render
from managers.serializers import AcceptManagerInviteSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


# Create your views here.


# Phase 1
@api_view(['POST'])
@permission_classes([AllowAny])
def accept_manager_invite(request):
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


