from django import forms
from .models import Order, Customer, Seller
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
    
    
    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username = uname).exists():
            raise forms.ValidationError("Username already exists.")
        
        return uname


class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    

class PasswordChangeForm(forms.Form):
    oldpassword = forms.CharField(widget=forms.PasswordInput())
    newpassword = forms.CharField(widget=forms.PasswordInput())
    confirmpassword = forms.CharField(widget=forms.PasswordInput())
    
    
class SellerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    
    class Meta:
        model = Seller
        fields = ["username","password","email","full_name", "mobile","address"]
    
    
    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username = uname).exists():
            raise forms.ValidationError("Username already exists.")
        
        return uname


# class UserProfileForm(forms.ModelForm):
#     phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}), required=False)
#     address = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}), required=False)
#     city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}), required=False)
#     state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}), required=False)
#     zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Zipcode'}), required=False)
#     country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}), required=False)
    
#     class Meta:
#         model = Profile
#         fields = ('phone', 'address', 'city', 'state', 'zipcode', 'country',)