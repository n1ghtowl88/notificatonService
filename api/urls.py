from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, MailingViewSet, MessageViewList


app_name = 'api'

router = DefaultRouter()
router.register('clients', ClientViewSet)
router.register('mailings', MailingViewSet)

urlpatterns = [
    path('v1/',
         include(router.urls)),
    path(r'v1/mailings/<int:mailing_id>/stat/',
         MessageViewList.as_view(),
         name='mailing_messages')
]
