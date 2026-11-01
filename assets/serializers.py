from rest_framework import serializers
from .models import Customer_RO_Purifier
from customers.models import CustomerUserProfile

class CustomerROPurifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_RO_Purifier
        fields = '__all__'
        read_only_fields = ('company',)

    def validate(self, data):
        company = self.context.get('company')
        # In PUT requests, the customer might not be in the data if not being updated
        customer = data.get('customer')

        if company and customer:
            # Ensure the customer belongs to the same company
            if customer.company != company:
                raise serializers.ValidationError(
                    {"customer": "The selected customer does not belong to this company."}
                )
        return data
