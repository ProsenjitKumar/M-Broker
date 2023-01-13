from django.urls import re_path
from .views import p2p_transfer_view

urlpatterns = [
    re_path('p2p-transfer/', p2p_transfer_view, name='p2p-transfer'),
]