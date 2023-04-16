from rest_framework import serializers
from .models import CustomUser,Customer

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email','password']
        model=CustomUser



   

class UserRegistrationSerializer(serializers.Serializer):
    email=serializers.CharField() 
    password =serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    full_name=serializers.CharField()
    address=serializers.CharField()

    class Meta:
        model=CustomUser
        fields='__all__'

    def validate(self,attrs):
        email=attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User already registered")
        return attrs

        
    
class ForgetPasswordSerializer(serializers.ModelSerializer):
    email=serializers.CharField()

    class Meta:
        fields=['email']
        model=CustomUser

    def validate(self,attrs):
        email=attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
                return attrs
        else:
            raise serializers.ValidationError("Email not rgegsiter")

    
        
