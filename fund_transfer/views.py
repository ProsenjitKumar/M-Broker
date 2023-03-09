from django.shortcuts import render, redirect
from .models import P2PTransfer
from .forms import P2PTransferForm
from django.contrib import messages
from mainapp.models import Referral
from .models import P2PTransfer
from django.contrib.auth.models import User

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core import mail

# Create your views here.


def p2p_transfer_view(request):
    form = P2PTransferForm(request.POST or None)
    referral = Referral.objects.get(account=request.user)
    balance = referral.balance
    my_address = referral.account_address
    print("My address: ",my_address)
    submit_amount = request.POST.get('amount')
    submit_receiver_address = request.POST.get('receiver_account_address')
    print("submitted Receiver address: ", submit_receiver_address)
    balance_transfer_email = "profile/withdrawal/balance-transfer-email.txt"

    context = {
        'form': form,
        'balance': balance,
    }
    connection = mail.get_connection()
    if form.is_valid():
        if float(submit_amount) <= float(balance):
            print("current Balance: ", balance)

            # credit receiver
            try:
                receiver = Referral.objects.get(account_address=submit_receiver_address)
                if receiver is not submit_receiver_address and my_address != submit_receiver_address:
                    receriver_user = User.objects.get(username=receiver.account)
                    print(receriver_user)
                    # print(receriver_user.email)
                    # if receriver_user.email:
                    print("receiver email", receriver_user.email)
                    c = {
                        "sender_email": request.user.email,
                        "receiver_email": receriver_user.email,
                        "user": request.user,
                        "receriver_user": receriver_user,
                        "submit_amount": submit_amount,
                    }
                    # balance_transfer_text = render_to_string(balance_transfer_email, c)
                    referral.decrease_balance(float(submit_amount))
                    email = EmailMessage(
                        'You got a new funds',
                        'you got new balance in your',
                        from_email=settings.EMAIL_HOST_USER,
                        to=[receriver_user.email],
                        bcc=['prosenjit.pq@gmail.com', 'faisal2001.ak@gmail.com'],
                        reply_to=['info@meekbroker.com'],
                        headers={'Message-ID': 'foo'},
                        connection=connection,
                    )
                    email.send()
                    confirm = form.save(commit=False)
                    confirm.user = request.user
                    print(request.user, 'sent you $',submit_amount)
                    print("Receiver : ", receiver)
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


def balance_transfer_history(request):
    object_list = P2PTransfer.objects.filter(user=request.user)
    context = {
        'object_list': object_list,
    }
    return render(request, 'profile/fund-transfer/balance-transfer-history.html', context)