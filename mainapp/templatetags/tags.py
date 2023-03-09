from django import template
from mainapp.models import Referral
import random
from django.http import JsonResponse

register = template.Library()

@register.simple_tag
def number_of_messages(request):

    referrals = Referral.objects.get(account=request.user)
    balance = referrals.balance
    return balance

@register.simple_tag
def mkb_coin(request):
    # mkb = round(random.uniform(0.000001, 0.0001), 4)
    # mkb = random.randrange(1000000) / 1000000000
    # if mkb > 0.0009:
    #     mkb = 0.0001
    st = 0.00001
    la = 0.0009
    # getting random float number between st to la
    mkb = st + (random.random()) * (la - st)
    return mkb