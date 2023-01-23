from django import forms
from django.utils.translation import gettext_lazy as _
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget

#models 
from base.models import userInfo
from .models import voucher, voucher_history

class signForm(forms.Form):
    signature = JSignatureField()
