from django.urls import re_path
from .views import investment_request_view, deposit_history

urlpatterns = [
    re_path('investment/', investment_request_view, name='investment'),
    re_path('deposit-history/', deposit_history, name='deposit-history'),
]