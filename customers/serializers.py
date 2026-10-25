from rest_framework import serializers
from .models import CustomerUserProfile
import uuid

class RegisterNewCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerUserProfile
        fields = [
            'name',
            'addressLine1',
            'addressLine2',
            'age',
            'alternate_contact',
            'city',
            'state',
            'country',
            'postal_code'
        ]

    def create(self, validated_data):
        user = self.context.get("user")
        company = self.context.get("company")

        if(not company):
            return serializers.ValidationError({'Company':"Company is missing from the context"})

        customer_code = f"{company.short_name}-CUST-{uuid.uuid4().hex[:6].upper()}"

        customer_profile = CustomerUserProfile.objects.create(
            user_id = user,
            company_id = company,
            customer_code = customer_code,
            **validated_data
        )

        return customer_profile