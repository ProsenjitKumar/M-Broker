from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class CryptoCoinList(models.Model):
    coin_name = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to="coin/logo/", null=True, blank=True)
    deposit_address = models.CharField(max_length=455, null=True, blank=True)
    qr_code_image = models.ImageField(upload_to="coin/qrcode/", null=True, blank=True)
    network = models.CharField(max_length=255, blank=True, null=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.coin_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.coin_name


