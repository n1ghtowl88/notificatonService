# Generated by Django 4.1.5 on 2023-01-30 09:57

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_mailing_end_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='end_datetime',
            field=models.DateTimeField(db_index=True, validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2023, 1, 30, 9, 57, 39, 794618, tzinfo=datetime.timezone.utc), message='Mailing end cannot be in the past')], verbose_name='Finish of mailing'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='start_datetime',
            field=models.DateTimeField(db_index=True, validators=[django.core.validators.MinValueValidator(limit_value=datetime.datetime(2023, 1, 30, 9, 57, 39, 794543, tzinfo=datetime.timezone.utc), message='Mailing start cannot be in the past')], verbose_name='Start of mailing'),
        ),
    ]
