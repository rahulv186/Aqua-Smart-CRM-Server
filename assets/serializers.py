from rest_framework import serializers
from .models import Customer_RO_Purifier
from customers.models import CustomerUserProfile

class CustomerROPurifierSerializer(serializers.ModelSerializer):
    # Make customer details readable if needed, or accept customer ID/profile on write
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Customer_RO_Purifier
        fields = [
            'id', 'model_number', 'serial_number', 'capacity', 
            'customer', 'customer_name', 'status', 'installation_date', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ('company', 'status', 'created_at', 'updated_at')

    def validate(self, data):
        company = self.context.get('company')
        customer = data.get('customer')

        if company and customer:
            # Ensure the assigned customer belongs to the same company workspace
            if customer.company != company:
                raise serializers.ValidationError(
                    {"customer": "The selected customer does not belong to this company workspace."}
                )
        return data