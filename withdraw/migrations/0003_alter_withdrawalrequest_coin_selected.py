# Generated by Django 4.0.2 on 2023-01-24 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0002_withdrawalrequest_network_selected_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='coin_selected',
            field=models.CharField(blank=True, choices=[('Bitcoin', 'Bitcoin'), ('USDT', 'USDT'), ('Ethereum', 'Ethereum'), ('BUSD', 'BUSD'), ('Dogecoin', 'Dogecoin'), ('BNB', 'BNB'), ('Litecoin', 'Litecoin'), ('USDC', 'USDC'), ('SOL Solana', 'SOL Solana'), ('BNB', 'BNB'), ('MATIC Polygon', 'MATIC Polygon'), ('XRP Ripple', 'XRP Ripple'), ('ADA Cardano', 'ADA Cardano')], max_length=25, null=True),
        ),
    ]
