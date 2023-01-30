import datetime as dt

from django.db.models import Q
from rest_framework import serializers

from .models import Client, Mailing, Message, STATUS_CHOICES


ONE_HOUR_DELTA = dt.timedelta(seconds=3600)


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ('id',
                  'start_datetime',
                  'text',
                  'tag',
                  'operator_code',
                  'end_datetime')

    def create(self, validated_data):
        start_datetime_obj = dt.datetime.strptime(
            self.initial_data['start_datetime'],
            '%Y-%m-%dT%H:%M:%SZ')
        end_datetime_obj = dt.datetime.strptime(
            self.initial_data['end_datetime'],
            '%Y-%m-%dT%H:%M:%SZ')
        if (end_datetime_obj - start_datetime_obj) >= ONE_HOUR_DELTA:
            mailing = Mailing.objects.create(**validated_data)
        else:
            raise serializers.ValidationError(f'The mailing minimum duration '
                                              f'should be 1 hour or more')
        tag = mailing.tag
        code = mailing.operator_code
        if tag != '' and code != '':
            clients = Client.objects.filter(Q(tag=tag) | Q(operator_code=code))
        elif tag == code == '':
            clients = Client.objects.all()
        elif tag == '' and code != '':
            clients = Client.objects.filter(operator_code=code)
        else:
            clients = Client.objects.filter(tag=tag)

        for client in clients:
            Message.objects.create(status=STATUS_CHOICES[0][0],
                                   mailing=mailing,
                                   client=client)
        return mailing


class MailingStatSerializer(serializers.ModelSerializer):
    mailing_id = serializers.IntegerField(source='id')
    all_messages = serializers.SerializerMethodField()
    ready = serializers.SerializerMethodField()
    sent = serializers.SerializerMethodField()
    failed = serializers.SerializerMethodField()
    not_sent = serializers.SerializerMethodField()

    class Meta:
        model = Mailing
        fields = ('mailing_id',
                  'all_messages',
                  STATUS_CHOICES[0][0],
                  STATUS_CHOICES[1][0],
                  STATUS_CHOICES[2][0],
                  STATUS_CHOICES[3][0]
                  )

    def get_all_messages(self, obj):
        return obj.messages.count()

    def get_ready(self, obj):
        return obj.messages.filter(status=STATUS_CHOICES[0][0]).count()

    def get_sent(self, obj):
        return obj.messages.filter(status=STATUS_CHOICES[1][0]).count()

    def get_failed(self, obj):
        return obj.messages.filter(status=STATUS_CHOICES[2][0]).count()

    def get_not_sent(self, obj):
        return obj.messages.filter(status=STATUS_CHOICES[3][0]).count()


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id',
                  'msisdn',
                  'operator_code',
                  'tag',
                  'time_zone')


class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.IntegerField(source='id')

    class Meta:
        model = Message
        fields = ('message_id',
                  'datetime',
                  'status',
                  'client')
