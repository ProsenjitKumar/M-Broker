from django.urls import re_path
from .views import main_view, signup_view, login_view, user_logout,\
    dashboard, ProfileView, affiliate_team, upcoming_view, account_info,\
    password_reset_request
from django.contrib.auth import views as auth_views #import this

urlpatterns = [
    re_path('^$', main_view, name='main_view'),
    # re_path('signup/', signup_view, name='signup'),
    re_path('signin/', login_view, name='signin'),
    re_path('logout/', user_logout, name='logout'),
    re_path('dashboard/', dashboard, name='dashboard'),
    re_path('profile/', ProfileView.as_view(), name='profile'),
    re_path('affiliate-team/', affiliate_team, name='affiliate-team'),
    re_path('account-info/', account_info, name='account-info'),
    re_path("password_reset", password_reset_request, name="password_reset"),
    re_path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='profile/signup/reset/password_reset_done.html'),
         name='password_reset_done'),
    re_path('reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/',
         auth_views.PasswordResetConfirmView.as_view(template_name="profile/signup/reset/password_reset_confirm.html"),
         name='password_reset_confirm'),
    re_path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='profile/signup/reset/password_reset_complete.html'),
         name='password_reset_complete'),

    re_path('upcoming/', upcoming_view, name='upcoming'),
]
