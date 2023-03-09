from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import Referral, Profile
from deposit.models import DepositRequestConfirmation, InvestmentRequest
from .forms import SignupForm, LoginForm, ProfileForm, form_validation_error,\
    ContactForm, KYCForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator

# password reset
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

import numpy as np
from django.views.decorators.cache import cache_page

#location
from django.contrib.gis.geoip2 import GeoIP2



# -------------------------------
#                                |
#           Main View
#                                |
# -------------------------------
# def base(request):
#     import random
#     mkb = round(random.uniform(0.00001, 0.0009), 6)
#     return JsonResponse(data={'mkb': mkb})


def main_view(request, *args, **kwargs):
    # g = GeoIP2()
    # print(g.country('google.com'))

    from deposit.views import getDepsoit
    getDepsoit(request)
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
    login_form = LoginForm(request.POST or None)
    context = {
        'form': form,
        'login_form': login_form,
    }
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Submitted!')
        return HttpResponseRedirect("/")

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return HttpResponseRedirect("/dashboard/")

        # return render(request, 'index/index.html', context)
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
#           Authentication View
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
    email_submitted = request.POST.get('email')
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
            send_mail('Thanks for joining with Meek Broker',
                      'An investment in knowledge pays the best interest.\n'
                      'Meek Broker is the platform where you will be able to make your dream successful.\n'
                      '\n'
                      'Web: www.meekbroker.com\n'
                      'Mail: company@gmail.com\n'
                      'Phone: +998 765 775 34',
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[email_submitted]
                      )
        else:
            print("Referral not working")
            form.save()
        username = form.cleaned_data.get('username')
        # email = form.cleaned_data.get('email')
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

# password reset
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "profile/signup/reset/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'company@meekbroker.com', [user.email], fail_silently=False)

                        messages.success(request,
                                         'A message with reset password instructions has been sent to your inbox.')
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    # return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="profile/signup/reset/password_reset.html", context={"password_reset_form":password_reset_form})

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
@cache_page(600)
@login_required(login_url='/signin/')
def dashboard(request):
    # base(request)
    # email_submitted = 'prosenjit.uar@gmail.com'
    # send_mail('Thanks for joining with Meek Broker',
    #           'An investment in knowledge pays the best interest.\n'
    #           'Meek Broker is the platform where you make your dream successfully.\n'
    #           'Mail: company@gmail.com\n'
    #           'Phone: +998 765 775 34',
    #           from_email=settings.EMAIL_HOST_USER,
    #           recipient_list=[email_submitted]
    #           )
    # print('email send to', email_submitted)
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

    # --------------- In template show value
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


def schedule_job():
    print("--------------Schedule Job Started--------------------------")

    print("* add balance and clearance *")

    referrals = Referral.objects.all()
    for toclearance in referrals:
        if toclearance.invested:
            last_roi = toclearance.roi_profit
            level_income = toclearance.level_income
            direct_refer = toclearance.direct_refer_income
            stored_level_income = toclearance.today_sell_volume
            print(" --------- user ---------- ", toclearance.account)
            print("current roi: ", last_roi)
            print("current direct refer: ", direct_refer)
            print("current level income: ", level_income)
            # toclearance.increase_balance(float(last_roi))
            print("increased ROI into main balance", last_roi)
            # toclearance.increase_balance(float(direct_refer))
            print("increased direct refer into main balance", direct_refer)

            # toclearance.update_roi_profit(float(0.00))
            print("Updated roi profit to 0.00", last_roi)
            # toclearance.update_today_sell_volume(float(0.00))

            # toclearance.update_refer_bonus(float(0.00))
            print("Updated direct refer bonus to 0.00")

            # toclearance.update_today_level_income(float(0.00))
            print("Updated level income to 0.00", level_income)

            if stored_level_income >= 10:
                # toclearance.increase_balance(float(level_income))
                print("increased level income into main balance", stored_level_income)
                # toclearance.update_today_sell_volume(float(0.00))
                print("Updated stored level income to 0.00", stored_level_income)

    # print("* ************* ROI Profit * ***************")
    # for ref in referrals:
    #     if ref.invested:
    #         # print("Ref account id = ", ref.account_id)
    #         ref_account = ref.account_id
    #         account = Referral.objects.get(account=ref_account)
    #         # print(account)
    #         investment = InvestmentRequest.objects.filter(user=ref_account)
    #         if investment:
    #             for invested in investment:
    #                 invested_amount = invested.amount
    #                 scheme = invested.scheme
    #                 current = datetime.now(timezone.utc).date()
    #                 day = 1
    #                 created = invested.created_at.date()
    #                 all_days = (created + timedelta(x + 1) for x in range((current - created).days))
    #                 days = sum(1 for day in all_days if day.weekday() < 5)
    #                 if days >= day:
    #                     if scheme == '1' and days <= 15:
    #                         print(" --------- ------- user: ", invested.user)
    #                         print("it's scheme 1")
    #                         print("Invested amount: ", invested_amount)
    #                         print("created: ", created)
    #                         print("days: ", days)
    #                         daily_profit = float(invested_amount) * 1 / 100
    #                         print("Daily Profit = ",daily_profit)
    #                         # ref.today_roi_profit(float(daily_profit))
    #                         # ref.increase_today_sell_volume(float(daily_profit))
    #                         # ref.increase_total_sell_volume(float(daily_profit))
    #                     elif scheme == '2' and days <= 30:
    #                         print(" --------- ------- user: ", invested.user)
    #                         print("it's scheme 2")
    #                         print("Invested amount: ", invested_amount)
    #                         print("created: ", created)
    #                         print("days: ", days)
    #                         daily_profit = float(invested_amount) * 1.5 / 100
    #                         print("Daily Profit = ", daily_profit)
    #                         # ref.today_roi_profit(float(daily_profit))
    #                         # ref.increase_today_sell_volume(float(daily_profit))
    #                         # ref.increase_total_sell_volume(float(daily_profit))
    #                     elif scheme == '3' and days <= 50:
    #                         print(" --------- ------- user: ", invested.user)
    #                         print("it's scheme 3")
    #                         print("Invested amount: ", invested_amount)
    #                         print("created: ", created)
    #                         print("days: ", days)
    #                         daily_profit = float(invested_amount) * 2 / 100
    #                         print("Daily Profit = ", daily_profit)
    #                         # ref.today_roi_profit(float(daily_profit))
    #                         # ref.increase_today_sell_volume(float(daily_profit))
    #                         # ref.increase_total_sell_volume(float(daily_profit))

    print("* ************  Level Income ********** *")

    for ref in referrals:
        if ref.invested:
            my_level = ref.level
            print("My Level = ", my_level)
            print("user: ", ref.account)
            ''' 
            if my level is 20
            need to count 20+1, 20+2 ... 20+10.
            so 20+1 = my first level 
            20+2 = my second level
            ...... 20+10 = my 10th level
            --------------- or another method
            if my level is 20
            how many level available in my downlines
            '''
            # print("----- level 1 ---------")
            level_1 = ref.get_descendants().filter(level=my_level + 1)
            level_2 = ref.get_descendants().filter(level=my_level + 2)
            level_3 = ref.get_descendants().filter(level=my_level + 3)
            level_4 = ref.get_descendants().filter(level=my_level + 4)
            level_5 = ref.get_descendants().filter(level=my_level + 5)
            level_6 = ref.get_descendants().filter(level=my_level + 6)
            level_7 = ref.get_descendants().filter(level=my_level + 7)
            level_8 = ref.get_descendants().filter(level=my_level + 8)
            level_9 = ref.get_descendants().filter(level=my_level + 9)
            level_10 = ref.get_descendants().filter(level=my_level + 10)

            print("----- level 1 ---------", level_1)
            for user in level_1:
                if user.invested:
                    print('Level 1', user)
                    total_income = user.roi_and_level_earning()
                    print("total income", total_income)
                    # print(user.balance)
                    level_1_commission = total_income * 8 / 100
                    print("Level 1 comission: ", level_1_commission)
                    # ref.today_level_income(float(level_1_commission))
                    print(level_1_commission, "comission added into today_level_income")
                    # ref.increase_today_sell_volume(float(level_1_commission))
                    print(level_1_commission, "comission added into increase_today_sell_volume")
                    # ref.increase_total_sell_volume(float(level_1_commission))
                    # print(level_1_commission, "comission added into increase_total_sell_volume")

            print("----- level 2 ---------", level_2)
            for user in level_2:
                if user.invested:
                    print('Level 2', user)
                    total_income = user.roi_and_level_earning()
                    print("total income", total_income)
                    # print(user.balance)
                    level_2_commission = total_income * 6 / 100
                    print("Level 2 comission: ", level_2_commission)
                    # ref.today_level_income(float(level_2_commission))
                    print(level_2_commission, "comission added into today_level_income")
                    # ref.increase_today_sell_volume(float(level_1_commission))
                    print(level_2_commission, "comission added into increase_today_sell_volume")
                    # ref.increase_total_sell_volume(float(level_2_commission))

            print("----- level 3 ---------", level_3)
            for user in level_3:
                if user.invested:
                    print('Level 3', user)
                    total_income = user.roi_and_level_earning()
                    print("total income", total_income)
                    # print(user.balance)
                    level_3_commission = total_income * 5 / 100
                    print("Level 3 comission: ", level_3_commission)
                    # ref.today_level_income(float(level_3_commission))
                    print(level_3_commission, "comission added into today_level_income")
                    # ref.increase_today_sell_volume(float(level_1_commission))
                    print(level_3_commission, "comission added into increase_today_sell_volume")
                    # ref.increase_total_sell_volume(float(level_3_commission))
            #
            # print("----- level 4 ---------", level_4)
            # for user in level_4:
            #     if user.invested:
            #         print(user)
            #         total_income = user.roi_and_level_earning()
            #         print("total income", total_income)
            #         # print(user.balance)
            #         level_4_commission = total_income * 4 / 100
            #         print("Level 4 comission: ", level_4_commission)
            #         ref.today_level_income(float(level_4_commission))
            #         ref.increase_total_sell_volume(float(level_4_commission))
            #
            # print("----- level 5 ---------", level_5)
            # for user in level_5:
            #     if user.invested:
            #         print(user)
            #         total_income = user.roi_and_level_earning()
            #         print("total income", total_income)
            #         # print(user.balance)
            #         level_5_commission = total_income * 3 / 100
            #         print("Level 5 comission: ", level_5_commission)
            #         ref.today_level_income(float(level_5_commission))
            #         ref.increase_total_sell_volume(float(level_5_commission))
            #
            # print("----- level 6 ---------", level_6)
            # for user in level_6:
            #     if user.invested:
            #         print(user)
            #         total_income = user.roi_and_level_earning()
            #         print("total income", total_income)
            #         # print(user.balance)
            #         level_6_commission = total_income * 2 / 100
            #         print("Level 6 comission: ", level_6_commission)
            #         ref.today_level_income(float(level_6_commission))
            #         ref.increase_total_sell_volume(float(level_6_commission))
            #
            # print("----- level 7 ---------", level_7)
            # for user in level_7:
            #     if user.invested:
            #         print(user)
            #         total_income = user.roi_and_level_earning()
            #         print("total income", total_income)
            #         # print(user.balance)
            #         level_7_commission = total_income * 1 / 100
            #         print("Level 7 comission: ", level_7_commission)
            #         ref.today_level_income(float(level_7_commission))
            #         ref.increase_total_sell_volume(float(level_7_commission))
            #
            # print("----- level 8 ---------", level_8)
            # for user in level_8:
            #     if user.invested:
            #         print(user)
            #         total_income = user.roi_and_level_earning()
            #         print("total income", total_income)
            #         # print(user.balance)
            #         level_8_commission = total_income * 0.7 / 100
            #         print("Level 8 comission: ", level_8_commission)
            #         ref.today_level_income(float(level_8_commission))
            #         ref.increase_total_sell_volume(float(level_8_commission))
            #
            # print("----- level 9 ---------", level_9)
            # for user in level_9:
            #     if user.invested:
            #         print(user)
            #         total_income = user.roi_and_level_earning()
            #         print("total income", total_income)
            #         # print(user.balance)
            #         level_9_commission = total_income * 0.5 / 100
            #         print("Level 9 comission: ", level_9_commission)
            #         ref.today_level_income(float(level_9_commission))
            #         ref.increase_total_sell_volume(float(level_9_commission))
            #
            # print("----- level 10 ---------", level_10)
            # for user in level_10:
            #     if user.invested:
            #         print(user)
            #         total_income = user.roi_and_level_earning()
            #         print("total income", total_income)
            #         # print(user.balance)
            #         level_10_commission = total_income * 0.3 / 100
            #         print("Level 10 comission: ", level_10_commission)
            #         ref.today_level_income(float(level_10_commission))
            #         ref.increase_total_sell_volume(float(level_10_commission))

    print(" **************** end ******************")

    # amar downnliner incomer 8 % pabo first generation
    # second generation - 6 %
    # third generation - 5 %
    # ---------- 10 th


scheduler = BackgroundScheduler()
job = None


def start_job():
    global job
    # job = scheduler.add_job(schedule_job, 'cron', day_of_week='mon-fri', hour=14, minute=5)
    job = scheduler.add_job(schedule_job, CronTrigger(day_of_week='mon-fri', hour=19, minute=58))
    # job = scheduler.add_job(schedule_job, 'interval', seconds=500)
    # sched.add_job(grabit, 'cron', day_of_week='mon-fri', hour=0, minute=13, id="get_things", replace_existing=True)
    try:
        scheduler.start()
    except:
        pass


start_job()

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

# -----------------------------------------------------

def how_it_works(request):
    return render(request, 'profile/dashboard/how-it-works.html')

def privacy_policy(request):
    return render(request, 'index/terms/privacy-policy.html')

def terms_conditions(request):
    return render(request, 'index/terms/terms-and-conditions.html')


# -------------------------------
#                                |
#           KYC View
#                                |
# -------------------------------
def kyc_view(request):
    form = KYCForm(request.POST, request.FILES or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Submitted!')
        return HttpResponseRedirect("/kyc/")
    return render(request, 'profile/settings/user_verification.html', context)




