from django import forms
from .models import PasswordEntry
from django.contrib.auth.models import User

class PasswordEntryForm(forms.ModelForm):
    shared_with = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = PasswordEntry
        fields = ['site_name', 'site_url', 'username', 'password', 'shared_with']
