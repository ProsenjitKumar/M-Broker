from django.shortcuts import render, get_object_or_404, redirect
from .models import CryptoCoinList
from deposit.models import DepositRequestConfirmation
from django.views.generic import ListView
from deposit.forms import DepositConfirmationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mainapp.models import Referral


# Create your views here.


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
    print("just deposited: ", submit_amount)
    balance = referral.balance

    context = {
        'object': object,
        'form': form,
    }

    if form.is_valid():
        referral.increase_balance(float(submit_amount))
        # latest_obj.update_selected_coin(balance)
        confirm = form.save(commit=False)
        confirm.user = request.user
        confirm.save()
        messages.success(request, 'Confirmation Send')
        print("just deposited after form: ", balance)

        return redirect('/dashboard/')
    return render(request, 'profile/cryptocoin/coin-detail.html', context)



