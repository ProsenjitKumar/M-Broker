from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from .models import Referral, Profile
from .forms import SignupForm, LoginForm, ProfileForm, form_validation_error,\
    ContactForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator


# -------------------------------
#                                |
#           Main View
#                                |
# -------------------------------

def main_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))

    try:
        profile = Referral.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id = ', profile.id)
        print("profile", profile)
    except:
        pass
    # print(request.session.get_expiry_date())
    form = ContactForm(request.POST or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Submitted!')
        return HttpResponseRedirect("/")

    return render(request, 'index/index.html',context)


def upcoming_view(request):
    return render(request, 'profile/upcoming/upcoming.html')


# @login_required
# def message_processor(request):
#     referrals = Referral.objects.get(account=request.user)
#     balance = referrals.balance
#     if request.user.is_authenticated:
#         referrals = Referral.objects.get(account=request.user)
#         balance = referrals.balance
#     else:
#         balance = referrals.balance
#     return {
#         'messages' : balance
#     }

# -------------------------------
#                                |
#           Signup View
#                                |
# -------------------------------
@csrf_protect
def signup_view(request):
    profile_id = request.session.get('ref_profile')
    print('profile_id = ', profile_id)
    form = SignupForm(request.POST or None)
    if form.is_valid():
        if profile_id is not None:
            recommended_by_profile = Referral.objects.get(id=profile_id)
            print("recommended_by_profile = ", recommended_by_profile)

            instance = form.save()
            print("instance saved = ", instance)
            registered_user = User.objects.get(id=instance.id)
            print("registered_user = ", registered_user)
            registered_profile = Referral.objects.get(account=registered_user)
            print("registered_profile = ", registered_profile)
            print("registered_profile.account = ", registered_profile.account)
            print("recommended_by_profile.parent_id = ", recommended_by_profile.parent_id)
            print("recommended_by_profile.parent = ", recommended_by_profile.parent)
            print("recommended_by_profile.account = ", recommended_by_profile.account)
            print(" -------- ** -----------")
            # registered_profile.parent_id = recommended_by_profile.account.pk
            registered_profile.parent_id = profile_id

            print("registered_profile.parent_id = ", registered_profile.parent_id)
            registered_profile.save()
            print("registered_profile it's saved = 100%", registered_profile)
        else:
            print("Referral not working")
            form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('dashboard')
    context = {
        'form': form
    }
    return render(request, 'profile/signup/register.html', context)


@csrf_protect
def login_view(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/dashboard/")
            else:
                messages.error(request, 'Your account is not active yet.')
                return render(request, 'profile/signup/login.html', context)
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            messages.error(request, 'Username or Password is not correct.')
            return render(request, 'profile/signup/login.html', context)
    else:
        return render(request, 'profile/signup/login.html', context)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    print("logout Successfully")

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


# -------------------------------
#                                |
#           Dashboard View
#                                |
# -------------------------------
@login_required(login_url='/signin/')
def dashboard(request):
    referrals = Referral.objects.get(account=request.user)
    last_login = User.objects.get(username=request.user)
    print(last_login.last_login)

    balance = referrals.balance
    context = {
        'balance': balance
    }
    return render(request, 'profile/dashboard/index.html', context)


# Profile Update
@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class ProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        return render(request, 'profile/dashboard/author-profile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)

        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('profile')


# Affiliate Team
@login_required(login_url='/signin/')
def affiliate_team(request):

    referrals = Referral.objects.get(account=request.user)
    family = referrals.get_family()
    direct_refers = referrals.get_children()
    total_members = referrals.get_descendant_count()
    total_downlines = referrals.get_descendants()
    aff_code = referrals.code
    acc_address = referrals.account_address

    context = {
        'family': family,
        'total_members': total_members,
        'direct_refers': direct_refers,
        'total_downlines': total_downlines,
        'aff_code': aff_code,
        'acc_address': acc_address,
    }

    return render(request, 'profile/dashboard/affiliate-team.html', context)


# -------------------------------
#                                |
#           Account Info View
#                                |
# -------------------------------

# Account Info
@login_required(login_url='/signin/')
def account_info(request):
    referrals = Referral.objects.get(account=request.user)
    aff_code = referrals.code
    acc_address = referrals.account_address

    context = {
        'aff_code': aff_code,
        'acc_address': acc_address,
    }

    return render(request, 'profile/dashboard/account-info.html', context)