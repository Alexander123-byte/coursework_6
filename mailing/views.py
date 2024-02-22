from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from blog.models import Blog
from mailing.forms import MailingForm, MessageForm, ManagerMailingForm, ClientForm
from mailing.models import Mailing, Message, Logs, Client
from django.urls import reverse_lazy
from django.http import Http404

from users.utils import UserRequiredMixin


def index(request):
    """
    Функция для отображения главной страницы
    """
    count_mailing = Mailing.objects.all()
    active_mailing = Mailing.objects.filter(mailing_status='launched')
    count_unique_client = Client.objects.values('client_email').distinct()
    articles = Blog.objects.order_by('?')[:3]
    context = {'count_mailing': count_mailing, 'active_mailing': active_mailing,
               'count_unique_client': count_unique_client, 'articles': articles}
    return render(request, 'users/index.html', context)


class MailingListView(LoginRequiredMixin, ListView):
    """
       Класс для отображения страницы со списком рассылок
    """
    model = Mailing

    def get_queryset(self):
        if self.request.user.has_perm('mailing.view_all_mailings'):
            mailing_list = super().get_queryset()
        else:
            mailing_list = super().get_queryset().filter(user_id=self.request.user)
        return mailing_list


class MailingCreateView(LoginRequiredMixin, UserRequiredMixin, CreateView):
    """Класс для создания рассылки"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для изменения рассылки"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_class(self):
        if self.request.user == self.object.user or self.request.user.is_superuser:
            return MailingForm
        elif self.request.user.has_perm('mailing.set_deactivate'):
            return ManagerMailingForm
        else:
            raise Http404('У вас нет прав на редактирование рассылок')


class MailingDetailView(UserRequiredMixin, DetailView):
    """Класс для просмотра отдельной рассылки"""

    model = Mailing
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset


class MailingDeleteView(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    """ Класс для удаления рассылки"""
    model = Mailing
    success_url = reverse_lazy('mailing:index')


class MessageListView(ListView):
    """
       Класс для отображения страницы со списком сообщений
    """
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Класс для создания сообщения для рассылки
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс для редактирования сообщения в рассылке
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDetailView(DetailView):
    """
    Класс для отображения страницы отдельного сообщения
    """
    model = Message

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс для удаления сообщения из рассылки
    """
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class ClientCreateView(LoginRequiredMixin, UserRequiredMixin, CreateView):
    """
    Класс для создания нового клиента для отправки рассылки
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс для редактирования клиента в рассылке
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


class ClientListView(UserRequiredMixin, ListView):
    """Класс для просмотра списка клиентов для рассылок"""
    model = Client


class ClientDetailView(UserRequiredMixin, DetailView):
    """Класс для просмотра отдельного клиента для рассылки"""
    model = Client


class ClientDeleteView(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    """Класс для удаления клиента для рассылки"""
    model = Client
    success_url = reverse_lazy('mailing:client_list')


class LogCreate(CreateView):
    """
    Класс для создания логов
    """
    model = Logs

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class LogsListView(LoginRequiredMixin, ListView):
    """
     Класс для вывода списка логов рассылок пользователя
     """
    model = Logs

    def get_queryset(self):
        """Метод для вывода логов только текущего пользователя"""
        return super().get_queryset().filter(user=self.request.user)
