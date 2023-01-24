from django.urls import re_path
from .views import withdrawal_request_view, withdrawal_history

urlpatterns = [
    re_path('withdraw/', withdrawal_request_view, name='withdraw'),
    re_path('withdraw-history/', withdrawal_history, name='withdraw-history'),
]