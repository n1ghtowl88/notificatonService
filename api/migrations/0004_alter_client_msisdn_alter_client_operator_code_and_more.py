# Generated by Django 4.1.5 on 2023-01-26 12:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_client_msisdn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='msisdn',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(code='invalid', message='Enter 7 digit number using the form 7(123)XXXXXXX', regex='^\\d{7}$')]),
        ),
        migrations.AlterField(
            model_name='client',
            name='operator_code',
            field=models.CharField(max_length=3, validators=[django.core.validators.RegexValidator(code='invalid', message='Enter a 3 digit number', regex='^\\d{3}$')]),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='operator_code',
            field=models.CharField(blank=True, max_length=3, validators=[django.core.validators.RegexValidator(code='invalid', message='Enter a 3 digit number', regex='^\\d{3}$')]),
        ),
    ]
