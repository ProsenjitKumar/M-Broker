# Generated by Django 4.0.2 on 2023-01-14 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0002_alter_depositrequestconfirmation_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositrequestconfirmation',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
