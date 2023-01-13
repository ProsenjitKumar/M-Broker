from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.apps import apps

from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import Referral, PinSet, Profile, Contact


@admin.register(Referral)
class ReferralAdmin(MPTTModelAdmin):
    list_filter = ['level']
    list_select_related = ['account', 'parent']
    search_fields = ['account__first_name', 'account__last_name']
    list_display = ['inner_id', 'account', 'parent', 'decendants', 'downlines', 'level', 'created_at', 'balance']

    def decendants(self, obj):
        return obj.get_descendant_count()

    def downlines(self, obj):
        return obj.downlines.count()

    def get_queryset(self, request):
        return super().get_queryset(request).only('inner_id', 'account', 'parent')


admin.site.register(PinSet)
admin.site.register(Profile)
admin.site.register(Contact)
