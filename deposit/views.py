from django.shortcuts import render, redirect
from .models import InvestmentRequest
from .forms import InvestmentRequestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mainapp.models import Referral
from .models import DepositRequestConfirmation

# Create your views here.


@login_required
def investment_request_view(request):
    form = InvestmentRequestForm(request.POST or None)
    referral = Referral.objects.get(account=request.user)
    balance = referral.balance
    submit_amount = request.POST.get('amount')
    context = {
        'form': form,
    }
    if form.is_valid():
        if float(submit_amount) <= float(balance):
            referral.decrease_balance(float(submit_amount))
            print("current Balance: ", balance)
            confirm = form.save(commit=False)
            confirm.user = request.user
            confirm.save()
            messages.success(request, 'Successfully Done!')
            return redirect('investment')
        else:
            print("Insufficient funds!")
            messages.error(request, 'Insufficient funds!')
    return render(request, 'profile/deposit/investment.html', context)


def deposit_history(request):
    object_list = DepositRequestConfirmation.objects.filter(user=request.user)

    context = {
        'object_list': object_list,
    }

    return render(request, 'profile/deposit/deposit-history.html', context)
