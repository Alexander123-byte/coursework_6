from django.utils import timezone
from django.db import models

from users.models import User


class Client(models.Model):
    """Модель клиента, получающего рассылки"""
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    client_email = models.EmailField(verbose_name='почта клиента')
    comment = models.CharField(max_length=300, verbose_name='комментарий', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец', null=True)

    def __str__(self):
        return f'{self.fullname} {self.client_email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        unique_together = (('owner', 'client_email',),)

class Message(models.Model):
    """Модель сообщения в рассылке"""
    title = models.CharField(max_length=150, verbose_name='тема сообщения')
    message = models.TextField(max_length=500, verbose_name='тело сообщения')

    def __str__(self):
        return f'{self.title}: {self.message}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    """Модель рассылки"""

    CHOICES_INTERVAL = [
        ('0', 'один раз'),
        ('1', 'ежедневно'),
        ('7', 'еженедельно'),
        ('30', 'ежемесячно'),
    ]
    STATUS_CHOICES = [
        ('completed', 'завершена'),
        ('created', 'создана'),
        ('launched', 'запущена'),
    ]
    mailing_name = models.CharField(max_length=100, verbose_name='название рассылки')
    create_date = models.DateField(default=timezone.now, verbose_name='дата и время создания рассылки')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='владелец рассылки')
    sent_time = models.DateField(default=timezone.now, null=True, blank=True,
                                 verbose_name='время отправки рассылки')
    mail_to = models.ManyToManyField(Client, verbose_name='клиенты')

    periodicity = models.CharField(max_length=50, choices=CHOICES_INTERVAL, default='',
                                   verbose_name='периодичность рассылки')

    mailing_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='created',
                                      verbose_name='статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, verbose_name='сообщение в рассылке')

    def __str__(self):
        return f'{self.mailing_name} / {self.sent_time} / {self.periodicity} / {self.mailing_status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            (
                'set_deactivate',
                'Can deactivate mailing'
            ),
        ]


class Logs(models.Model):
    """Модель логов рассылки"""
    TRY_STATUS_CHOICES = [
        ('success', 'успешно'),
        ('fail', 'неуспешно'),
    ]

    mailing_name = models.ForeignKey(Mailing, on_delete=models.SET_NULL, null=True, verbose_name='имя рассылки')
    last_try_date = models.DateField(blank=True, null=True, verbose_name='время последней попытки')
    try_status = models.CharField(max_length=30, choices=TRY_STATUS_CHOICES, verbose_name='статус попытки',
                                  default='', blank=True, null=True)
    server_response = models.CharField(max_length=300, null=True, blank=True, verbose_name='ответ сервера')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='пользователь сервиса')

    def __str__(self):
        return f'{self.mailing_name}: {self.last_try_date} {self.try_status} {self.user} - {self.server_response}'

    class Meta:
        verbose_name = 'попытка отправки'
        verbose_name_plural = 'попытки отправки'



