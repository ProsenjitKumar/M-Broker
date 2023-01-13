from django.contrib import admin
from .models import P2PTransfer

# Register your models here.


class P2PTransferAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'receiver_account_address', 'active', 'updated_at', 'created_at',]
    search_fields = ['receiver_account_address',]
    list_per_page = 30


admin.site.register(P2PTransfer, P2PTransferAdmin)
