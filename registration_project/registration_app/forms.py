from dataclasses import field
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField 
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email_id = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    class Meta:
        model = User
        fields = '__all__'
