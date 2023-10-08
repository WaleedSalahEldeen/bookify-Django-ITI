from django import forms
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PasswordChangeForm(forms.Form):
    def __init__(self, user,):
        self.user = user

    old_password = forms.CharField(label='Old Password')
    new_password = forms.CharField(label='New Password')
    confirm_password = forms.CharField(label='Confirm New Password')
