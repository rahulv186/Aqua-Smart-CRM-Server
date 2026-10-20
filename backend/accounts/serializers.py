from rest_framework import serializers

from django.contrib.auth import get_user_model

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
        user = User.objects.create(
            email = validated_data['email'],
            phone = validated_data['phone'],
            full_name = validated_data['full_name'],
            password = validated_data['password']
        )
        return user