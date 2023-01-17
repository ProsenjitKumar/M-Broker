from django import forms
from django.forms import TextInput
from .models import DepositRequestConfirmation, InvestmentRequest,\
    INVESTMENT_SELECT


# -------------------------------
#                                |
#     Deposit Confirmation Form
#                                |
# -------------------------------


class DepositConfirmationForm(forms.ModelForm):
    class Meta:
        model = DepositRequestConfirmation
        fields = '__all__'
        exclude = ['user', 'active', 'balance',]

        widgets = {
            'amount_deposited': TextInput(attrs={'placeholder': 'Amount'}),
            'transaction_id': TextInput(attrs={'placeholder': 'Transaction ID'}),

        }


class InvestmentRequestForm(forms.ModelForm):
    scheme = forms.ChoiceField(choices=INVESTMENT_SELECT, required=True)
    class Meta:
        model = InvestmentRequest
        fields = '__all__'
        exclude = ['user', 'active',]

        widgets = {
            'amount': TextInput(attrs={'placeholder': 'Amount'}),
        }