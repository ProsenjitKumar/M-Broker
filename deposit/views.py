from django.shortcuts import render, redirect
from .models import InvestmentRequest
from .forms import InvestmentRequestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mainapp.models import Referral
from .models import DepositRequestConfirmation
from django.http import JsonResponse

# Create your views here.


@login_required
def investment_request_view(request):
    form = InvestmentRequestForm(request.POST or None)
    referral = Referral.objects.get(account=request.user)
    balance = referral.balance
    submit_amount = request.POST.get('amount')
    submit_scheme = request.POST.get('scheme')
    # get upline refer id
    myUpline = referral.parent_id
    print(" My upline id  ", myUpline)
    if myUpline:
        refer_receiver = Referral.objects.get(id=myUpline)
        print(" My refer receiver: ", refer_receiver)
        # if refer_receiver.invested:
        #     print("Invested")
        # else:
        #     print("not investor")
    context = {
        'form': form,
    }
    p1 = 20.00
    p2 = 150.00
    p3 = 350.00
    if form.is_valid():
        if float(submit_amount) <= float(balance) and float(submit_amount) >= float(p1):
            print("current Balance: ", balance)

            if submit_scheme == '1' and float(submit_amount) >= float(p1):
                if myUpline or True:

                    referral.decrease_balance(float(submit_amount))
                    refer_bonus = float(submit_amount) * 2 / 100
                    invested = True
                    referral.update_invested(invested)

                    try:
                        refer_receiver = Referral.objects.get(id=myUpline)
                        print(" My refer receiver: ", refer_receiver)
                        if refer_receiver.invested:
                            print("upline account is active")
                            refer_receiver.increase_refer_bonus(float(refer_bonus))
                            # refer_receiver.increase_balance(float(refer_bonus))
                            refer_receiver.increase_total_sell_volume(float(refer_bonus))
                    except:
                        pass

                    print("Scheme: ", submit_scheme)
                    messages.success(request, 'Successfully Done!')
            elif submit_scheme == '2' and float(submit_amount) >= float(p2):
                if myUpline or True:

                    referral.decrease_balance(float(submit_amount))
                    refer_bonus = float(submit_amount) * 5 / 100
                    invested = True
                    referral.update_invested(invested)

                    try:
                        refer_receiver = Referral.objects.get(id=myUpline)
                        print(" My refer receiver: ", refer_receiver)
                        refer_receiver.increase_refer_bonus(float(refer_bonus))
                        # refer_receiver.increase_balance(float(refer_bonus))
                        refer_receiver.increase_total_sell_volume(float(refer_bonus))
                    except:
                        pass

                    print("Scheme: ", submit_scheme)
                    messages.success(request, 'Successfully Done!')
            elif submit_scheme == '3' and float(submit_amount) >= float(p3):
                if myUpline or True:

                    referral.decrease_balance(float(submit_amount))
                    refer_bonus = float(submit_amount) * 10 / 100
                    invested = True
                    referral.update_invested(invested)

                    try:
                        refer_receiver = Referral.objects.get(id=myUpline)
                        print(" My refer receiver: ", refer_receiver)
                        refer_receiver.increase_refer_bonus(float(refer_bonus))
                        # refer_receiver.increase_balance(float(refer_bonus))
                        print("total sell start")
                        refer_receiver.increase_total_sell_volume(float(refer_bonus))
                        print("total sell submitted")
                    except:
                        pass

                    print("Scheme: ", submit_scheme)
                    messages.success(request, 'Successfully Done!')
            else:
                messages.error(request, 'Insufficient funds for this package!')
            confirm = form.save(commit=False)
            confirm.user = request.user
            confirm.save()

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


def investment_history(request):
    object_list = InvestmentRequest.objects.filter(user=request.user)

    context = {
        'object_list': object_list,
    }

    return render(request, 'profile/deposit/investment-history.html', context)


def getDepsoit(request):
    # queryset = DepositRequestConfirmation.objects.all()
    queryset = DepositRequestConfirmation.objects.all().order_by('-id')[:3]
    # users = list(queryset.values())
    users = queryset.values()
    # for user in users:
        # print(user.user.username)
        # print(type(user))
    return JsonResponse({'users':list(queryset.values())})