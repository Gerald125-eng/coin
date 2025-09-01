from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class UpdatePasswordForm(PasswordChangeForm):
    pass




class DepositForm(forms.Form):
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
    ]

    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    crypto_type = forms.ChoiceField(choices=CRYPTO_CHOICES, widget=forms.RadioSelect)

