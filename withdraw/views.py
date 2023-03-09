from django.shortcuts import render, redirect
from .models import WithdrawalRequest
from mainapp.models import Referral
from .forms import WithdrawalRequestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core import mail


# Create your views here.


@login_required
def withdrawal_request_view(request):
    form = WithdrawalRequestForm(request.POST or None)
    referral = Referral.objects.get(account=request.user)
    balance = referral.balance
    receiver_email = request.user.email
    print(receiver_email)
    print('previus balance: ', balance)
    submit_amount = request.POST.get('withdraw_amount')
    min_withdraw = 20
    c = {
        "email": request.user.email,
        "user": request.user,
        "submit_amount": submit_amount,
    }
    admin_email_template = "profile/withdrawal/admin-email.txt"
    admin_email_text = render_to_string(admin_email_template, c)
    context = {
        'form': form,
        'balance': balance,
    }
    connection = mail.get_connection()
    if form.is_valid():
        if float(submit_amount) <= float(balance) and float(submit_amount) >= float(min_withdraw):
            referral.decrease_balance(float(submit_amount))
            print("current Balance: ", balance)
            print("Withdraw succesfully")
            confirm = form.save(commit=False)
            confirm.user = request.user
            confirm.save()
            messages.success(request, 'Confirmation Send')
            email = EmailMessage(
                'Your withdraw has been successfully done!',
                admin_email_text,
                from_email=settings.EMAIL_HOST_USER,
                to = [receiver_email],
                bcc = ['prosenjit.pq@gmail.com', 'faisal2001.ak@gmail.com'],
                reply_to=['info@meekbroker.com'],
                headers={'Message-ID': 'foo'},
                connection=connection,
            )
            email.send()
            # send_mail('Your withdraw has been successfully done!',
            #           admin_email_text,
            #           from_email=settings.EMAIL_HOST_USER,
            #           recipient_list=[email, 'prosenjit.pq@gmail.com', 'kateyalide@gmail.com',],
            #           fail_silently=False,
            #           )

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
