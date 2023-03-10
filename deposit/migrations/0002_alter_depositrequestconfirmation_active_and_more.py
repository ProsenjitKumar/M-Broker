# Generated by Django 4.0.2 on 2023-01-14 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositrequestconfirmation',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='investmentrequest',
            name='scheme',
            field=models.CharField(blank=True, choices=[('1', '15 Working Days Profit 1% Up To 2% Min. $20 Up To.'), ('2', '30 Working Days Profit 1.5% Up To Min. 3% $200 Up To'), ('3', '50 Working Days Profit 2% Up To 4% Min. $500 Up To')], max_length=100, null=True),
        ),
    ]
