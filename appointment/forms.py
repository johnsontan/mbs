from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

#models
from .models import appointment_available_dates, appointment, appointment_service

#custom validators


class setAvailDate(forms.ModelForm):
    class Meta:
        model = appointment_available_dates
        fields = ['employee', 'avail_date']
