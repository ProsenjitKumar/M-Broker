# Generated by Django 4.0.2 on 2023-01-24 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0005_alter_depositrequestconfirmation_coin_selected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositrequestconfirmation',
            name='coin_selected',
            field=models.CharField(blank=True, choices=[('Bitcoin', 'Bitcoin'), ('USDT', 'USDT'), ('Ethereum', 'Ethereum'), ('BUSD', 'BUSD'), ('Dogecoin', 'Dogecoin'), ('BNB', 'BNB'), ('Litecoin', 'Litecoin'), ('USDC', 'USDC'), ('SOL Solana', 'SOL Solana'), ('BNB', 'BNB'), ('MATIC Polygon', 'MATIC Polygon'), ('XRP Ripple', 'XRP Ripple'), ('ADA Cardano', 'ADA Cardano')], max_length=25, null=True),
        ),
    ]
