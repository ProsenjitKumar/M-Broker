from django.urls import re_path
from .views import CryptoCoinListView, coin_detail_view, HomeView, ChartData

urlpatterns = [
    re_path('coin-list/', CryptoCoinListView.as_view(), name='coin-list'),
    re_path('coin-details/(?P<slug>[-\w]+)/', coin_detail_view, name='coin-details'),
    re_path('coin/', HomeView.as_view()),
    re_path('api/', ChartData.as_view()),
]