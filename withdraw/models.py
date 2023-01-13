from django.db import models
from django.contrib.auth.models import User

# Create your models here.

COIN_SELECTED = (
    ('1', 'Bitcoin'),
    ('2', 'Litecoin'),
    ('3', 'Ethereum'),
)


class WithdrawalRequest(models.Model):
    user = models.ForeignKey(User, related_name="withdraw_request", on_delete=models.CASCADE)
    withdraw_amount = models.DecimalField(max_digits=15, decimal_places=2)
    coin_selected = models.CharField(max_length=25, choices=COIN_SELECTED, null=True, blank=True)
    coin_address = models.CharField(max_length=450, null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.withdraw_amount}"
