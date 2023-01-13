from django.contrib import admin
from .models import DepositRequestConfirmation, InvestmentRequest

# Register your models here.


class DepositConfirmationAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount_deposited', 'active', 'updated_at', 'created_at',]
    search_fields = ['amount_deposited',]
    list_per_page = 30


admin.site.register(DepositRequestConfirmation, DepositConfirmationAdmin)


class InvestmentRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'active', 'updated_at', 'created_at',]
    search_fields = ['amount',]
    list_per_page = 30


admin.site.register(InvestmentRequest, InvestmentRequestAdmin)
