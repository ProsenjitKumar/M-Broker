from django.shortcuts import render, redirect
from .models import P2PTransfer
from .forms import P2PTransferForm
from django.contrib import messages
from mainapp.models import Referral

# Create your views here.


def p2p_transfer_view(request):
    form = P2PTransferForm(request.POST or None)
    referral = Referral.objects.get(account=request.user)
    balance = referral.balance
    submit_amount = request.POST.get('amount')
    submit_receiver_address = request.POST.get('receiver_account_address')
    print("submitted Receiver address: ", submit_receiver_address)

    context = {
        'form': form,
        'balance': balance,
    }
    if form.is_valid():
        if float(submit_amount) <= float(balance):
            print("current Balance: ", balance)

            # credit receiver
            try:
                receiver = Referral.objects.get(account_address=submit_receiver_address)
                if receiver is not submit_receiver_address:
                    referral.decrease_balance(float(submit_amount))
                    confirm = form.save(commit=False)
                    confirm.user = request.user
                    print("Receiver: ", receiver)
                    receiver.increase_balance(float(submit_amount))
                    receiver.save()
                    # debit sender save
                    confirm.save()
                    messages.success(request, 'Successfully Transferred!')
                    print("Withdraw succesfully")
                else:
                    messages.error(request, 'Invalid Address')
                    print("Invalid Address")
            except:
                messages.error(request, 'Invalid Address')

            return redirect('/p2p-transfer/')
        else:
            print("insufficient funds!")
            messages.error(request, 'Insufficient funds')

    return render(request, 'profile/fund-transfer/p2p.html', context)
