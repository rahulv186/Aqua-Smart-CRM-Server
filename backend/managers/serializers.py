from sys import exception

from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.utils import generate_unique_code
from managers.models import ManagerUserProfile
from invitation.models import Invitation
User = get_user_model()


class AcceptManagerInviteSerializer(serializers.ModelSerializer):
    token = serializers.UUIDField()
    password = serializers.CharField(write_only = True, min_length = 8)
    phone = serializers.CharField()

    def validate_token(self, value):

        try:
            invitation = Invitation.objects.get(token = value)

        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid Token")

        if not invitation.is_valid():
            raise serializers.ValidationError("Invite Link Expired or Used")

        self.invitation = invitation
        return value
    def save(self, **kwargs):

        invitation = self.invitation

        # Create User
        user = User.objects.create_user(
            email = invitation.email,
            phone = self.validated_data['phone'],
            password=self.validated_data['password']
        )

        # Create Manager Profile
        manager_profile = ManagerUserProfile(
            user = user,
            company = invitation.company,
            employee_code = generate_unique_code(ManagerUserProfile, "employee_code", "EMP", 4),
            is_active = True
        )

        invitation.is_accepted = True
        invitation.save()

        return user


class ManagerProfileOnboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerUserProfile
        fields = (
            'name',
            'addressLine1',
            'addressLine2',
            'city',
            'state',
            'country',
            'postal_code',
            '',
            '',
            ''
        )