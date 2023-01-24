from django.db import models
from django.contrib.auth.models import User

# Create your models here.

COIN_SELECTED = (
    ('Bitcoin', 'Bitcoin'),
    ('USDT', 'USDT'),
    ('Ethereum', 'Ethereum'),
    ('BUSD', 'BUSD'),
    ('Dogecoin', 'Dogecoin'),
    ('BNB', 'BNB'),
    ('Litecoin', 'Litecoin'),
    ('USDC', 'USDC'),
    ('SOL Solana', 'SOL Solana'),
    ('BNB', 'BNB'),
    ('MATIC Polygon', 'MATIC Polygon'),
    ('XRP Ripple', 'XRP Ripple'),
    ('ADA Cardano', 'ADA Cardano'),
)

NETWORK_SELECTED = (
    ('BTC Bitcoin', 'BTC Bitcoin'),
    ('Ethereum (ERC20)', 'Ethereum (ERC20)'),
    ('LTC Litecoin', 'LTC Litecoin'),
    ('Tron (TRC20)', 'Tron (TRC20)'),
    ('BNB Smart Chain (BEP20)', 'BNB Smart Chain (BEP20)'),
    ('Cardano ', 'Cardano '),
    ('Polygon ', 'Polygon '),
    ('SOL Solana', 'SOL Solana'),
    ('DOGE Dogecoin', 'DOGE Dogecoin'),
)


class WithdrawalRequest(models.Model):
    user = models.ForeignKey(User, related_name="withdraw_request", on_delete=models.CASCADE)
    withdraw_amount = models.DecimalField(max_digits=15, decimal_places=2)
    coin_selected = models.CharField(max_length=25, choices=COIN_SELECTED, null=True, blank=True)
    network_selected = models.CharField(max_length=25, choices=NETWORK_SELECTED, null=True, blank=True)
    coin_address = models.CharField(max_length=450, null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.withdraw_amount}"
