from app.models import OrderPlaced, Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs=
        {'autocomplete':'current-password', 'class':'form-control'}))

class update_product(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = ['status']
        label = {'status':'Process'}