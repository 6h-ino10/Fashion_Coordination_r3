from django import forms
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile,Region

class UserChangeForm(BaseUserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput(),required=False)

    class Meta:
        model = User
        fields = ['username','email','password']

class RegionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['region']

    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label='地域を選択')

