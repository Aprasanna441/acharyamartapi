from rest_framework import serializers
from .models import CustomUser,Customer,Product,Cart,CartProduct,Order
from django.contrib.auth import authenticate

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





class UserChangePasswordSerializer(serializers.Serializer):
    oldpassword=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    
    class Meta:
        fields=['oldpassword','password','password2']
        model=CustomUser

    def validate(self, attrs):
        user=self.context.get('user')
        print(user,"usar")
        password=attrs.get('password')
        oldpassword=attrs.get('oldpassword')
        password2=attrs.get('password2')
        user=authenticate(email=user,password=oldpassword)
        # print(user)
        if password!=password2:
            raise serializers.ValidationError("Password and confirm password didnt match")
        elif user is not None :        
            user.set_password(password)
            user.save()
        else:
            return serializers.ValidationError("User doesnt exist")
        return  attrs
           

class AllProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class CategoricalProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class AddProductsSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
        model=Product


class AddToCartSerializer(serializers.ModelSerializer):
    customer=serializers.CharField()
    product_id=serializers.IntegerField()
    class Meta:
        model=Cart
        fields=['customer','product_id']

class MyCartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Cart
        fields="__all__"
    

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['order_by','shipping_address','mobile','email','payment_method']
