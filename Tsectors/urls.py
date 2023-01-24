"""Tsectors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from mainapp.views import main_view, signup_view
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from admin_notification.views import check_notification_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    # path('', include('django.contrib.auth.urls')),
    path('', include('cryptocoin.urls')),
    path('', include('withdraw.urls')),
    path('', include('deposit.urls')),
    path('', include('fund_transfer.urls')),
    path('check/notification', check_notification_view, name="check_notifications"),

    # path('signup/<str:ref_code>/', main_view, name='main-view'),
    # path('<str:ref_code>/', main_view, name='main-view'),
    path('signup/<str:ref_code>/', signup_view, name='signup'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'mainapp.views.error_404'
