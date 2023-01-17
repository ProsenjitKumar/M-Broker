from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect, HttpResponse
from .models import Referral, Profile
from deposit.models import DepositRequestConfirmation, InvestmentRequest
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
def signup_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))

    try:
        profile = Referral.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id = ', profile.id)
        print("profile", profile)
    except:
        pass
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
# import time
# from timeloop import Timeloop
# from datetime import timedelta
#
# tl = Timeloop()
# @tl.job(interval=timedelta(seconds=5))
@login_required(login_url='/signin/')
def dashboard(request):
    print('dashboard')
    referrals = Referral.objects.get(account=request.user)
    last_login = User.objects.get(username=request.user)
    # print("call Dask cluster 300s job current time : {}".format(time.ctime()))
    # tl.start()
    # print(last_login.last_login)
    # scheduler.shutdown()

    # deposit active
    deposit = DepositRequestConfirmation.objects.filter(user=request.user)
    if deposit:
        early_deposited = deposit.latest('created_at')
        early_deposited_amount = early_deposited.amount_deposited
        balance = referrals.balance
        # print("current Balance: ", balance)
        # print("All deposited: ", deposit)
        # print("Early deposited: ", early_deposited)
        # print("Early deposited amount: ", early_deposited_amount)
        updated_deposited = early_deposited.updated_at
        updated_referral_balance = referrals.updated_at
        print("Updated at deposit", updated_deposited)
        print("Updated at balance", updated_referral_balance)
        if early_deposited.active and early_deposited.updated_at:
            print("activated")
            referrals.increase_balance(early_deposited_amount)
            active = False
            early_deposited.update_active(active)

            print("successfully added")
        else:
            print("not activated yet")

    # Level Income
    downlines = referrals.get_descendants().filter(level__lte=referrals.level + 2)
    print("Level", downlines)

    # amar downnliner incomer 8 % pabo first generation
    # second generation - 6 %
    # third generation - 5 %
    # ---------- 10 th

    # ROI Profit


    balance = referrals.balance
    roi_profit = referrals.roi_profit
    refer_bonus = referrals.direct_refer_income
    level_income = referrals.level_income

    context = {
        'balance': balance,
        'roi_profit': roi_profit,
        'refer_bonus': refer_bonus,
        'level_income': level_income,
    }
    return render(request, 'profile/dashboard/index.html', context)

# -------------------------------
#                                |
#           Django Schedule Job
#                                |
# -------------------------------
class Profit(View):
    def get(self, request):
        # referrals = Referral.objects.get(account=request.user)
        # print(referrals)
        print('its class')
        return None

def roi_profit(request):
    referrals = Referral.objects.get(account=request.user)
    print(referrals)
    # dashboard(request)

scheduler = BackgroundScheduler()
job = None
from rest_framework.request import HttpRequest, Request

def tick():
    print('One tick!')
    obj = Profit()
    # make http request object
    http_request_obj = HttpRequest()
    # make http request object
    request = Request(http_request_obj)
    query_output_data = obj.get(request)

    # redirect(dashboard)
    # HttpResponseRedirect('/dashboard/')
    # dashboard(request='prosenjit')
    # return data

def start_job():
    global job
    job = scheduler.add_job(tick, 'interval', seconds=3)
    try:
        scheduler.start()
    except:
        pass


# start_job()

# -------------------------------
#                                |
#           Django Schedule Job End
#                                |
# -------------------------------

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
    # start_job()
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


# -------------------------------
#                                |
#           404 View
#                                |
# -------------------------------
def error_404(request, exception):
    return render(request, 'profile/error/404.html')