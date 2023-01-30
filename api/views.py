from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Client, Mailing
from .serializers import (ClientSerializer,
                          MailingSerializer,
                          MailingStatSerializer,
                          MessageSerializer)


class MailingViewSet(ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tag', 'operator_code']

    @action(detail=False, url_path='stat')
    def get_mailing_stat(self, request):
        mailings = Mailing.objects.all()
        serializer = MailingStatSerializer(mailings, many=True)
        return Response(serializer.data)


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tag', 'operator_code', 'time_zone']


class MessageViewList(ListAPIView):
    serializer_class = MessageSerializer

    def get_mailing(self):
        """Getting the mailing object by the mailing id"""
        return get_object_or_404(
            Mailing,
            id=self.request.parser_context['kwargs'].get('mailing_id'))

    def get_queryset(self):
        mailing = self.get_mailing()
        return mailing.messages.all()
