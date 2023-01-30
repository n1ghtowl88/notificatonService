from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

import pytz

STATUS_CHOICES = (
    ('ready', 'Ready to send'),
    ('sent', 'Sent'),
    ('failed', 'Failed to send'),
    ('not_sent', 'Not sent'),
)
TIMEZONES_CHOICES = tuple(zip(pytz.common_timezones, pytz.common_timezones))


class Mailing(models.Model):
    start_datetime = models.DateTimeField(
        verbose_name='Start of mailing',
        db_index=True,
        validators=[MinValueValidator(limit_value=timezone.now(),
                                      message=(f'Mailing start cannot be '
                                               f'in the past'))]
    )
    text = models.CharField(
        max_length=300
    )
    tag = models.CharField(
        max_length=15,
        blank=True
    )
    operator_code = models.CharField(
        max_length=3,
        validators=[RegexValidator(regex=r"^\d{3}$",
                                   message='Enter a 3 digit number',
                                   code='invalid')],
        blank=True
    )
    end_datetime = models.DateTimeField(
        verbose_name='Finish of mailing',
        db_index=True,
        validators=[MinValueValidator(limit_value=timezone.now(),
                                      message=(f'Mailing end cannot be '
                                               f'in the past'))]
    )


class Client(models.Model):
    msisdn = models.CharField(
        max_length=7,
        validators=[RegexValidator(regex=r"^\d{7}$",
                                   message=(f'Enter 7 digit number using '
                                            f'the form 7(123)XXXXXXX'),
                                   code='invalid')]
    )
    operator_code = models.CharField(
        max_length=3,
        validators=[RegexValidator(regex=r"^\d{3}$",
                                   message='Enter a 3 digit number',
                                   code='invalid')],
    )
    tag = models.CharField(
        max_length=15,
        blank=True
    )
    time_zone = models.CharField(
        max_length=32,
        default='UTC',
        choices=TIMEZONES_CHOICES
    )


class Message(models.Model):
    datetime = models.DateTimeField(
        verbose_name='Creation or sending datetime',
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='messages'
    )
