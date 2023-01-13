from django.contrib import admin
from .models import Login, EmailLogin, PhoneNumber
from django import forms
from django.forms import TextInput

# Register your models here.


class LoginAdmin(admin.ModelAdmin):
    list_display = ['username']
    list_per_page = 50


# admin.site.register(Login, LoginAdmin)


class EmailLoginAdmin(admin.ModelAdmin):
    list_display = ['email']
    list_per_page = 50


# admin.site.register(EmailLogin, EmailLoginAdmin)


class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ['phone_number']
    list_per_page = 50


# admin.site.register(PhoneNumber, PhoneNumberAdmin)


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = '__all__'

        widgets = {
            'phone_number': TextInput(attrs={'placeholder': 'Your Phone Number'}),

        }



class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = '__all__'

        widgets = {
            'username': TextInput(attrs={'placeholder': 'email@address.com'}),
            'password': TextInput(attrs={"type": "password", 'placeholder': 'Password'}),

        }


class EmailLoginForm(forms.ModelForm):
    class Meta:
        model = EmailLogin
        fields = '__all__'

        widgets = {
            'email': TextInput(attrs={'placeholder': 'email@address.com'}),
            'password': TextInput(attrs={"type": "password", 'placeholder': 'Password'}),

        }