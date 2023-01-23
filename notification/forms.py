from django import forms
from .models import notification, ack_notification
from base.models import userInfo
from django.utils.translation import gettext_lazy as _
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class sendNotification(forms.ModelForm):
    notification_title = forms.CharField(label="Subject")
    notification_description = forms.CharField(label="Description" ,widget=forms.Textarea)
    class Meta:
        model = notification
        fields = ['notification_title', 'notification_description']
