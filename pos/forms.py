from django import forms
import datetime
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus.widgets import DatePickerInput

#models 
from .models import sales_services,sales_transaction
from base.models import userInfo
from employee.models import employee_info

class searchPosbyDate(forms.Form):
    start_date = forms.DateField(widget=DatePickerInput())
    end_date = forms.DateField(widget=DatePickerInput(), required=False)
    employees = forms.ModelChoiceField(queryset=userInfo.objects.filter(role=2), required=False)
    

    