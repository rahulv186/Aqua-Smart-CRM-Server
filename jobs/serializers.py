from rest_framework import serializers
from jobs.models import ServiceTicket
from customers.models import CustomerUserProfile
class ServiceTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTicket
        fields = '__all__'
        read_only_fields = ["id", "company", "created_at", "updated_at"]


class CreateServiceTicketForStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTicket
        fields = ["ticket_type", "customer", "purifier", "issue_description"]

    def create(self, validated_data):
        # Get company from serializer context (passed securely from the view)
        company = self.context.get('company')
        if not company:
            raise serializers.ValidationError({"error": "Company context is missing."})

        customer = validated_data.get('customer')
        purifier = validated_data.get('purifier')

        if customer.company != company or purifier.company != company:
            raise serializers.ValidationError(
                {"detail": "Customer or purifier does not belong to this company workspace."}
            )

        # Ensure purifier belongs to the customer
        if purifier.customer != customer:
            raise serializers.ValidationError(
                {"purifier": "The selected purifier does not belong to this customer."}
            )

        return ServiceTicket.objects.create(
            company=company,
            **validated_data
        )


class CreateServiceTicketForCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTicket
        fields = ["ticket_type", "purifier", "issue_description"]

    def create(self, validated_data):
        company = self.context.get('company')
        request_user = self.context.get('request').user

        if not company:
            raise serializers.ValidationError({"error": "Company context is missing."})

        # Get the customer profile specific to this company workspace
        try:
            customer_profile = request_user.customer_user_profile # or CustomerUserProfile.objects.get(user=request_user, company=company)
        except Exception:
            raise serializers.ValidationError({"detail": "Customer profile not found for this user/company."})

        purifier = validated_data.get('purifier')

        # Validate that the purifier belongs to this company AND belongs to this logged-in customer
        if purifier.company != company or purifier.customer != customer_profile:
            raise serializers.ValidationError(
                {"purifier": "This purifier is not registered to your account in this workspace."}
            )

        return ServiceTicket.objects.create(
            company=company,
            customer=customer_profile,
            **validated_data
        )