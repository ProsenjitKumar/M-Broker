from django import template
from mainapp.models import Referral

register = template.Library()

@register.simple_tag
def number_of_messages(request):

    referrals = Referral.objects.get(account=request.user)
    balance = referrals.balance
    return balance