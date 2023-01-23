from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import userInfo, profile_pic, contact
from django.utils.translation import gettext_lazy as _
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    dob = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(required=True, max_length=8, min_length=8, validators=[RegexValidator(r'^\d{1,10}$')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def clean_check_renewal_date(self):
        data = self.cleaned_data['dob']

        #check if data is !> today
        if data >= datetime.date.today():
            raise ValidationError(_('Invalid Date of Birth'))

        return data
        
    class Meta:
        model = userInfo
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'dob', 'phone']

class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:        
        model = userInfo
        fields = ['email', 'password']


class UpdateAccountInfo(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True, max_length=8, min_length=8, validators=[RegexValidator(r'^\d{1,10}$')])
    dob =forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = userInfo
        fields = ['first_name', 'last_name', 'phone', 'dob']

class UpdateProfilePic(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = profile_pic
        fields = ['image']

class contactform(forms.ModelForm):
    cemail = forms.EmailField(label="Email")
    cphone = forms.CharField(label="Phone number", max_length=8, min_length=8, validators=[RegexValidator(r'^\d{1,10}$')])
    class Meta:
        model = contact
        fields = ['name', 'cemail', 'cphone', 'message']

class UpdateUserPassword(forms.ModelForm):
    oldPassword = forms.CharField(label="Old password",widget=forms.PasswordInput())
    password1 = forms.CharField(label="New password",widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm new password",widget=forms.PasswordInput())

    class Meta:
        model = userInfo
        fields = ['oldPassword', 'password1', 'password2']