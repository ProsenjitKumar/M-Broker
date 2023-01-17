import decimal
import uuid
import enum
from django.db import models
from django.utils import timezone, translation
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django_numerators.models import NumeratorMixin
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

_ = translation.gettext_lazy
from .utils import generate_ref_code, generate_coin_address
from django.templatetags.static import static

# Create your models here.


'''
******************
Referral
******************
'''


class Referral(NumeratorMixin, MPTTModel, models.Model):
    class Meta:
        verbose_name = _('Referral')
        verbose_name_plural = _('Referral')
        unique_together = ('parent', 'account')

    limit = 10

    parent = TreeForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='downlines',
        verbose_name=_('Up Line'))
    account = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_('account'))
    balance = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=2,
        editable=False,
        verbose_name=_("Balance"))

    roi_profit = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)
    total_roi_profit = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)
    level_income = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)
    total_level_income = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)
    direct_refer_income = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)
    total_direct_refer_income = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)
    meek_profit = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)
    rank_profit = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)
    today_sell_volume = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)
    total_sell_volume = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)
    trading_balance = models.DecimalField(default=0,max_digits=15,decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(
        default=timezone.now, editable=False)
    code = models.CharField(max_length=12, blank=True)
    account_address = models.CharField(max_length=60, blank=True, null=True)
    active = models.BooleanField(default=True)
    invested = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    # slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return (
            self.account.username
            if self.account.get_full_name() in ['', None]
            else self.account.get_full_name()
        )

    def update_balance(self, balance):
        self.balance = balance
        self.save()

    def decrease_balance(self, balance):
        self.balance -= decimal.Decimal(balance)
        self.save()

    def increase_balance(self, balance):
        self.balance += decimal.Decimal(balance)
        self.save()

    def increase_roi_profit(self, roi_profit):
        self.roi_profit += decimal.Decimal(roi_profit)
        self.save()

    def increase_total_roi_profit(self, total_roi_profit):
        self.total_roi_profit += decimal.Decimal(total_roi_profit)
        self.save()

    def increase_refer_bonus(self, direct_refer_income):
        self.direct_refer_income += decimal.Decimal(direct_refer_income)
        self.save()

    def update_invested(self, invested):
        self.invested = invested
        self.save()

    def get_referral_limit(self):
        return getattr(settings, 'REFERRAL_DOWNLINE_LIMIT', None) or self.limit

    def get_uplines(self):
        return self.get_ancestors(include_self=False, ascending=True)[:self.get_referral_limit()]

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            account_address = generate_coin_address()
            self.account_address = account_address
            self.code = code
        super().save(*args, **kwargs)



'''
******************
Settings
******************
'''


class PinSet(models.Model):
    user = models.OneToOneField(User, related_name="pin", on_delete=models.CASCADE)
    pin1 = models.IntegerField(blank=True, null=True)
    pin2 = models.IntegerField(blank=True, null=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


# ----------------------------
#
#          Profile
#
# ----------------------------
class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="customers/profiles/avatars/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('assets/img/team/default-profile-picture.png')

    def __str__(self):
        return self.user.username


'''
******************
Contact and Support
******************
'''


class Contact(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


