from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db import transaction
from django.utils.crypto import get_random_string
from core.utils import generate_unique_code
from hr.models import HRUserProfile
class CreateHRProfile(serializers.Serializer):
    email = serializers.EmailField()
    phone = serializers.CharField()
    # password = serializers.CharField(write_only = True, required=False)


    name = serializers.CharField(max_length=255)
    # employee_code = serializers.CharField(max_length=50)
    department = serializers.CharField(max_length=100, required=False, allow_blank=True)
    emergency_contact = serializers.CharField(max_length=20, required=False, allow_blank=True)
    addressLine1 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    addressLine2 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    postal_code = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError({"error":"User Already Exists with this Email"})
        return value

    @transaction.atomic
    def create(self, validated_data):
        company = validated_data.pop('company')

        auto_gen_password = get_random_string(length=8)
        employee_code = generate_unique_code(HRUserProfile, "employee_code", "TEC", 4)

        user = User.objects.create_user(
            email=validated_data['email'],
            password=auto_gen_password,
            phone = validated_data['phone']
        )

        hr_profile = HRUserProfile.objects.create(
            user=user,
            company=company,
            employee_code=employee_code,
            name = validated_data['name'],
            department=validated_data.get('department', ''),
            emergency_contact=validated_data.get('emergency_contact', ''),
            addressLine1=validated_data.get('addressLine1', ''),
            addressLine2=validated_data.get('addressLine2', ''),
            city=validated_data.get('city', ''),
            state=validated_data.get('state', ''),
            country=validated_data.get('country', ''),
            postal_code=validated_data.get('postal_code', ''),
            is_active = True,
            is_boarded = True,
        )

        return user, auto_gen_password, hr_profile

    