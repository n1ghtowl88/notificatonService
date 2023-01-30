# Generated by Django 4.1.5 on 2023-01-26 11:18

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_message_client_alter_message_mailing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='msisdn',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\d+)*\\Z'), code='invalid', message='Enter 7 digit number using the form 7(123)XXXXXXX')]),
        ),
    ]