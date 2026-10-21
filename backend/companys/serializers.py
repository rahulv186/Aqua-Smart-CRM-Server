from rest_framework import serializers
from companys.models import Company


class CreateNewCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = (
            'company_name',
            'slug',
            'short_name',
            'phone',
            'email',
            'gstin',
            'address',
            'city',
            'state',
            'country',
            'postal_code',
            'timezone',
            'currency',
            'plan',
            'plan_start_date',
            'plan_end_date',
            'payment_status',
            'is_active',
        )
    def validate_slug(self, value):
        if Company.objects.filter(slug=value).exists():
            raise serializers.ValidationError("This Slug is already taken.")
        return value
    
    def create(self, validated_data):
        company = Company.objects.create(
            **validated_data
        )
        return company
        

