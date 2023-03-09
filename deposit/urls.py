from django.urls import re_path
from .views import investment_request_view, deposit_history, investment_history,\
    getDepsoit

urlpatterns = [
    re_path('investment/', investment_request_view, name='investment'),
    re_path('deposit-history/', deposit_history, name='deposit-history'),
    re_path('investment-history/', investment_history, name='investment-history'),
    re_path('get-deposit/', getDepsoit, name='get-deposit'),
]