from django import forms
from django.utils.translation import gettext_lazy as _
import datetime
#models
from base.models import userInfo
from .models import employee_info

class employeeInfo(forms.ModelForm):
    sg_address = forms.CharField(label="Singapore address", required=False)
    my_address = forms.CharField(label="Malaysia address", required=False)
    wp_id = forms.CharField(label="Work permit ID", required=False)
    inner_role = forms.CharField(label="Employee role", required=False)
    class Meta:
        model = employee_info
        fields = ['sg_address', 'my_address', 'wp_id']
