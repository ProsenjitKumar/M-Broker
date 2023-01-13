from django.urls import re_path
from .views import withdrawal_request_view

urlpatterns = [
    re_path('withdraw/', withdrawal_request_view, name='withdraw'),
]