# Generated by Django 4.0.2 on 2023-01-18 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0004_depositrequestconfirmation_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositrequestconfirmation',
            name='coin_selected',
            field=models.CharField(blank=True, choices=[('1', 'Bitcoin'), ('2', 'USDT'), ('3', 'Ethereum'), ('3', 'BUSD'), ('4', 'Dogecoin'), ('5', 'BNB'), ('6', 'Litecoin'), ('7', 'USDC'), ('8', 'SOL Solana'), ('9', 'BNB'), ('10', 'MATIC Polygon'), ('11', 'XRP Ripple'), ('12', 'ADA Cardano')], max_length=25, null=True),
        ),
    ]
