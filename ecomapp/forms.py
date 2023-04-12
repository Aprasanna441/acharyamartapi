from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser,Order,Customer
from django.contrib.auth import authenticate


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=["order_by","shipping_address","mobile","email","payment_method"]


class CustomerRegistrationForm(forms.ModelForm):
    email=forms.CharField(widget=forms.TextInput())
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=Customer
        fields=["email","password","full_name","address"]

    def clean_email(self):
        email=self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.Proceed to login")
        return email



class CustomerLoginForm(forms.ModelForm):
    email=forms.CharField(widget=forms.TextInput())
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=Customer
        fields=["email","password"]

            
class ForgetPasswordForm(forms.Form):
    email=forms.CharField(widget=forms.EmailInput)

    def clean_email(self):
        email=self.cleaned_data.get("email")
        
        if CustomUser.objects.filter(email=email).exists():
            pass
        else:
            raise forms.ValidationError("Email entered for non registered customer")
        return email
    

class ResetPasswordForm(forms.Form):
    new_password=forms.CharField(widget=forms.PasswordInput)
    confirm_passwordconfirm=forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        np=self.cleaned_data.get("new_password")
        cp=self.cleaned_data.get("confirm_password")
        if np !=cp :
            raise forms.ValidationError("Pw and conf pw doesnt match")
        return cp
        

class ChangePasswordForm(forms.Form):
    email=forms.CharField(widget=forms.EmailInput)
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password=forms.CharField(widget=forms.PasswordInput)
    confirm_new_password=forms.CharField(widget=forms.PasswordInput)


        




    


    
    

    
