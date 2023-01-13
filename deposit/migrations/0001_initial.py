# Generated by Django 4.0.2 on 2023-01-13 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme', models.CharField(blank=True, choices=[('1', '15 Working Days Profit 1% Up To 2%'), ('2', '30 Working Days Profit 1.5% Up To 3%'), ('3', '50 Working Days Profit 2% Up To 4%')], max_length=100, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investment_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DepositRequestConfirmation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_deposited', models.DecimalField(decimal_places=2, max_digits=15)),
                ('coin_selected', models.CharField(blank=True, choices=[('1', 'Bitcoin'), ('2', 'Litecoin'), ('3', 'Ethereum')], max_length=25, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=450, null=True)),
                ('balance', models.FloatField(blank=True, null=True)),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposit_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
