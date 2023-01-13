from django import forms
from django.forms import TextInput
from .models import P2PTransfer


class P2PTransferForm(forms.ModelForm):
    class Meta:
        model = P2PTransfer
        fields = '__all__'
        exclude = ('user', 'active')

        widgets = {
            'receiver_account_address': TextInput(attrs={'placeholder': 'Receiver account address'}),
            'amount': TextInput(attrs={'placeholder': 'Amount'}),

        }
