from django.contrib import admin
from .models import WithdrawalRequest

# Register your models here.


class WithdrawAdmin(admin.ModelAdmin):
    list_display = ['user', 'withdraw_amount', 'active', 'updated_at', 'created_at', ]
    search_fields = ['withdraw_amount', ]
    list_per_page = 30


admin.site.register(WithdrawalRequest, WithdrawAdmin)
