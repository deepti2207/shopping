from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer, Product
from django.forms import TextInput, fields


#Registration Form
class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':"form-control"}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':"form-control"}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':"form-control"}))
    phone_no = forms.IntegerField(required=True, max_value=10,widget=forms.NumberInput(attrs={'class':"form-control"}))

    class Meta:
        model = User
        fields = ['username','email','phone_no','password1','password2']
        label = {'email':'Email'}
        widget = {'username':forms.TextInput(attrs={'class':'form-control'})}

#Vendors Registration form



#Login Form
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs=
        {'autocomplete':'current-password', 'class':'form-control'}))


#Change Password Form
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=('Old Password'),strip=False, widget=forms.PasswordInput
        (attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))

    new_password1 = forms.CharField(label=('New Password'),strip=False, widget=forms.PasswordInput
        (attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.
        password_validators_help_text_html())

    new_password2 = forms.CharField(label=('Confirm New Password'),strip=False, widget=forms.PasswordInput
        (attrs={'autocomplete':'new-password','class':'form-control'}))


# Reset Password Form
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=('Email'),max_length=255, widget=forms.EmailInput
        (attrs={'autocomplete':'email','class':'form-control'}))


#Confirm Reset Password Form
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=('New Password'),strip=False, widget=forms.PasswordInput
        (attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.
        password_validators_help_text_html())
    new_password2 = forms.CharField(label=('Confirm New Password'),strip=False, widget=forms.PasswordInput
        (attrs={'autocomplete':'new-password','class':'form-control'}))




class CustomerProfileform(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                'locality':forms.TextInput(attrs={'class':'form-control'}),
                'city':forms.TextInput(attrs={'class':'form-control'}),
                'state':forms.Select(attrs={'class':'form-control'}),
                'zipcode':forms.NumberInput(attrs={'class':'form-control'})

        }


class Product_Form(forms.ModelForm):
    class Meta:
        model = Product
        fields=['title','selling_price','description','discounted_price','brand','category','product_image']