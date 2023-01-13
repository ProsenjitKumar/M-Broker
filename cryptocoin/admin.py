from django.contrib import admin
from .models import CryptoCoinList

# Register your models here.


class CryptoCoinListAdmin(admin.ModelAdmin):
    list_display = ('coin_name', 'deposit_address',)
    exclude = ('slug',)


admin.site.register(CryptoCoinList, CryptoCoinListAdmin)
