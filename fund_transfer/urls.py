from django.urls import re_path
from .views import p2p_transfer_view, balance_transfer_history

urlpatterns = [
    re_path('p2p-transfer/', p2p_transfer_view, name='p2p-transfer'),
    re_path('p2p-transfer-history/', balance_transfer_history, name='p2p-transfer-history'),
]