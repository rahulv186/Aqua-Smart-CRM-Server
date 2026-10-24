from rest_framework import serializers
from companys.models import Company, CompanyOwnerProfile
from accounts.models import User
from django.utils.crypto import get_random_string
from django.db import transaction
from core.utils import generate_unique_code


class CreateNewCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "company_name",
            "slug",
            "short_name",
            "phone",
            "email",
            "gstin",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "timezone",
            "currency",
            "plan",
            "plan_start_date",
            "plan_end_date",
            "payment_status",
            "is_active",
        )

    def validate_slug(self, value):
        if Company.objects.filter(slug=value).exists():
            raise serializers.ValidationError("This Slug is already taken.")
        return value

    def create(self, validated_data):
        company_email = validated_data["email"]
        company_slug = validated_data["slug"]

        # FIX 1: RAISE the ValidationError instead of returning it
        if User.objects.filter(email=company_email).exists():
            raise serializers.ValidationError(
                {"email": "A User with this email already exists."}
            )

        generatedPassword = get_random_string(length=12)
        owner_username = f"owner-{company_slug}"

        with transaction.atomic():
            company = Company.objects.create(**validated_data)

            # FIX 2: Use create_user() so Django securely hashes the password!
            company_owner_user = User.objects.create_user(
                email=company_email,
                password=generatedPassword,
                full_name=owner_username,  # Assuming full_name is on your User model
            )

            company_owner_profile = CompanyOwnerProfile.objects.create(
                user=company_owner_user,
                company=company,
                employee_code=generate_unique_code(
                    CompanyOwnerProfile, "employee_code", "EMP", 4
                ),
            )

            self.generated_password = generatedPassword
            self.email = company_email

        return company


class CreateCompanyOwnerProfile(serializers.ModelSerializer):
    class Meta:
        model = CompanyOwnerProfile
        fields = (
            'name',
            'address',
            'date_of_birth',
            'city',
            'state',
            'country',
            'postal_code',
            'alternate_contact'
        )
        read_only_fields = ('user', 'employee_code', 'company')