from rest_framework import serializers
from .models import CustomUser

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email','password']
        model=CustomUser
