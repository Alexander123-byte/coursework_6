from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import MailingCreateView, MailingListView, MailingUpdateView, MailingDetailView, \
    MailingDeleteView, index, MessageListView, MessageCreateView, MessageUpdateView, MessageDetailView, \
    MessageDeleteView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientDetailView, ClientListView, \
    LogsListView

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('mailing/mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/detail/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('update_message/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_confirm_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing/client_create/', ClientCreateView.as_view(), name='client_create'),
    path('mailing/<int:pk>/client_update/', ClientUpdateView.as_view(), name='client_update'),
    path('mailing/<int:pk>/client_delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('mailing/client/<int:pk>/', ClientDetailView.as_view(), name='client'),
    path('mailing/client_list/', ClientListView.as_view(), name='client_list'),
    path('mailing/logs_list/', LogsListView.as_view(), name='logs_list'),

]
