from rest_framework import serializers

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from django.contrib.auth.models import update_last_login

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required = True,
        style = {"input_type" : "password"}
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'phone', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            phone = validated_data['phone'],
            full_name = validated_data['full_name'],
            password = validated_data['password']
        )
        return user


class SuperUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # 1. Let SimpleJWT do its normal job (check username and password)
        data = super().validate(attrs)
        
        # 2. 🔒 OUR CUSTOM RULE: Check if this user is a system superuser
        if not self.user.is_superuser:
            raise exceptions.PermissionDenied("Access denied. Only system superusers can log in here.")
            
        return data

class TenantEmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Updates the last_login timestamp automatically!
        update_last_login(None, self.user)
        
        return data