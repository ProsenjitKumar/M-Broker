from django.urls import re_path
from .views import main_view, signup_view, login_view, user_logout,\
    dashboard, ProfileView, affiliate_team, upcoming_view, account_info

urlpatterns = [
    re_path('^$', main_view, name='main_view'),
    re_path('signup/', signup_view, name='signup'),
    re_path('signin/', login_view, name='signin'),
    re_path('logout/', user_logout, name='logout'),
    re_path('dashboard/', dashboard, name='dashboard'),
    re_path('profile/', ProfileView.as_view(), name='profile'),
    re_path('affiliate-team/', affiliate_team, name='affiliate-team'),
    re_path('account-info/', account_info, name='account-info'),

    re_path('upcoming/', upcoming_view, name='upcoming'),
]
