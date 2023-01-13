from django.urls import re_path
from .views import CryptoCoinListView, coin_detail_view

urlpatterns = [
    re_path('coin-list/', CryptoCoinListView.as_view(), name='coin-list'),
    re_path('coin-details/(?P<slug>[-\w]+)/', coin_detail_view, name='coin-details'),
]