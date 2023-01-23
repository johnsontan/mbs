from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
#models
from base.models import userInfo
from .models import services, news, testimonial_pic

class userCreationFormA(UserCreationForm):
    email = forms.EmailField(required=True)
    dob = forms.DateField(required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(required=True, max_length=8, min_length=8, validators=[RegexValidator(r'^\d{1,10}$')])
    role = forms.ChoiceField(choices=userInfo.ROLE_CHOICES)

    def clean_check_renewal_date(self):
        data = self.cleaned_data['dob']

        #check if data is !> today
        if data >= datetime.date.today():
            raise ValidationError(_('Invalid Date of Birth'))

        return data
        
    class Meta:
        model = userInfo
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'dob', 'phone', 'role']

class userSuspend(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = userInfo
        fields = ['email']

class serviceform(forms.ModelForm):
    class Meta: 
        model = services
        fields = ["service_name", "service_description", "service_tnc", "service_price", "department"]

class newform(forms.ModelForm):
    class Meta:
        model = news
        fields = ["news_title", "news_description"]

class testimonialPic(forms.ModelForm):
    class Meta:
        model = testimonial_pic
        fields = ["image", "name"]