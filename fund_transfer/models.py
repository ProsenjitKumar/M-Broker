from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class P2PTransfer(models.Model):
    user = models.ForeignKey(User, related_name="p2p_transfer", on_delete=models.CASCADE)
    receiver_account_address = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.amount}"
