from django.db import models
from django.contrib.auth.models import User
from withdraw.models import COIN_SELECTED

# Create your models here.


class DepositRequestConfirmation(models.Model):
    user = models.ForeignKey(User, related_name="deposit_request", on_delete=models.CASCADE)
    amount_deposited = models.DecimalField(max_digits=15,decimal_places=2)
    coin_selected = models.CharField(max_length=25, choices=COIN_SELECTED, null=True, blank=True)
    transaction_id = models.CharField(max_length=450, null=True, blank=True)
    balance = models.FloatField(blank=True, null=True)

    active = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.amount_deposited}"

    def update_selected_coin(self, balance):
        self.balance = balance
        self.save()

    def update_active(self, active):
        self.active = active
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


INVESTMENT_SELECT = (
    ('1', '15 Working Days Profit 1% Up To 2% Min. $20 Up To.'),
    ('2', '30 Working Days Profit 1.5% Up To Min. 3% $200 Up To'),
    ('3', '50 Working Days Profit 2% Up To 4% Min. $500 Up To'),
)


class InvestmentRequest(models.Model):
    user = models.ForeignKey(User, related_name="investment_request", on_delete=models.CASCADE)
    scheme = models.CharField(max_length=100, choices=INVESTMENT_SELECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.amount}"


