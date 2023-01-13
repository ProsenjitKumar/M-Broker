from django import forms
from django.forms import TextInput
from .models import WithdrawalRequest


class WithdrawalRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = '__all__'
        exclude = ('user', 'active')

        widgets = {
            'withdraw_amount': TextInput(attrs={'placeholder': 'Amount'}),
            'coin_address': TextInput(attrs={'placeholder': 'Coin Address'}),
        }