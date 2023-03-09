from django.shortcuts import render, get_object_or_404, redirect
from .models import CryptoCoinList
from deposit.models import DepositRequestConfirmation
from django.views.generic import ListView
from deposit.forms import DepositConfirmationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mainapp.models import Referral

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core import mail

# mkbcoin import
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
# mkbcoin
class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index/mkbcoin.html')


####################################################

## if you don't want to user rest_framework

# def get_data(request, *args, **kwargs):
#
# data ={
#             "sales" : 100,
#             "person": 10000,
#     }
#
# return JsonResponse(data) # http response


#######################################################

## using rest_framework classes

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
        ]
        chartLabel = "my data"
        chartdata = [0, 10, 5, 2, 20, 30, 45, 23, 36]
        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": chartdata,
        }
        return Response(data)


# others views
class CryptoCoinListView(ListView):
    model = CryptoCoinList
    template_name = 'profile/cryptocoin/cryptocoinlist.html'


@login_required
def coin_detail_view(request, slug, *args, **kwargs):
    object = get_object_or_404(CryptoCoinList, slug=slug)
    print('object', object)
    referral = Referral.objects.get(account=request.user)
    print("referral user", referral)
    print("=", referral)
    depsoit_obj = DepositRequestConfirmation.objects.filter(user=request.user)
    # latest_obj = depsoit_obj.latest('created_at')
    # print(latest_obj)

    form = DepositConfirmationForm(request.POST or None)

    submit_amount = request.POST.get('amount_deposited')
    transaction_id = request.POST.get('transaction_id')
    print("just deposited: ", submit_amount)
    balance = referral.balance
    email = request.user.email

    c = {
        "email": email,
        "user": request.user,
        "submit_amount": submit_amount,
        "transaction_id": transaction_id,
    }
    email_template = "profile/cryptocoin/deposit-email.txt"
    email_text = render_to_string(email_template, c)

    context = {
        'object': object,
        'form': form,
    }
    connection = mail.get_connection()
    if form.is_valid():
        # referral.increase_balance(float(submit_amount))
        # latest_obj.update_selected_coin(balance)
        confirm = form.save(commit=False)
        confirm.user = request.user
        confirm.save()
        messages.success(request, 'Successfully Deposit Requested!')
        email = EmailMessage(
            'Your deposit request has been successfully done!',
            email_text,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            bcc=['prosenjit.pq@gmail.com', 'kateyalide@gmail.com'],
            reply_to=['info@meekbroker.com'],
            headers={'Message-ID': 'foo'},
            connection=connection,
        )
        email.send()
        print("just deposited after form: ", balance)

    return render(request, 'profile/cryptocoin/coin-detail.html', context)






