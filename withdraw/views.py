from django.shortcuts import render, redirect
from .models import WithdrawalRequest
from mainapp.models import Referral
from .forms import WithdrawalRequestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def withdrawal_request_view(request):
    form = WithdrawalRequestForm(request.POST or None)
    referral = Referral.objects.get(account=request.user)
    balance = referral.balance
    print('previus balance: ', balance)
    submit_amount = request.POST.get('withdraw_amount')
    min_withdraw = 20

    context = {
        'form': form,
        'balance': balance,
    }
    if form.is_valid():
        if float(submit_amount) <= float(balance) and float(submit_amount) >= float(min_withdraw):
            referral.decrease_balance(float(submit_amount))
            print("current Balance: ", balance)
            print("Withdraw succesfully")
            confirm = form.save(commit=False)
            confirm.user = request.user
            confirm.save()
            messages.success(request, 'Confirmation Send')
            return redirect('/withdraw/')
        else:
            print("insufficient funds! Minimum Withdraw $20.")
            messages.error(request, 'insufficient funds! Minimum Withdraw $20.')

    return render(request, 'profile/withdrawal/withdrawal-request.html', context)


def withdrawal_history(request):
    history = WithdrawalRequest.objects.filter(user=request.user)
    context = {
        'history': history,
    }
    return render(request, 'profile/withdrawal/withftawal-history.html', context)
