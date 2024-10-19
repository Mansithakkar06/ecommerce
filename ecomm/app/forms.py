from django import forms
from .models import Order, Customer
from django.contrib.auth.models import User


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ordered_by","shipping_address","mobile","email"]
        
        
class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    
   
    
    class Meta:
        model = Customer
        fields = ["username","password","email","full_name", "address"]