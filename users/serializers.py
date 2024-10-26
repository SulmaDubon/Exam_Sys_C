
# users/serializers.py

from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'second_last_name', 'phone_number', 'cedula', 'university', 'registration_date', 'state']
        read_only_fields = ['id', 'username', 'registration_date']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value
    
    def validate_cedula(self, value):
        if CustomUser.objects.filter(cedula=value).exists():
            raise serializers.ValidationError("A user with that cedula already exists.")
        return value
