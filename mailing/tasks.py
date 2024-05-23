from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.db.models import F
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.core.mail import send_mail
from datetime import datetime, timezone, timedelta
from mailing.models import Mailing, Logs
from config import settings
import smtplib


def start_mailing():
    """Функция запуска рассылки"""
    now = datetime.now(timezone.utc)
    mailing_list = Mailing.objects.filter(sent_time__lte=now)
    for mailing in mailing_list:
        title = mailing.message.title
        message = mailing.message.message

        try:
            send_mail(
                subject=title,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.client_email for client in mailing.mail_to.all()],
                fail_silently=False,
            )
            if mailing.periodicity == '0':
                mailing.sent_time = None
                mailing.mailing_status = 'completed'
            elif mailing.periodicity == '1':
                mailing.sent_time = F('sent_time') + timedelta(days=1)
                mailing.mailing_status = 'launched'
            elif mailing.periodicity == '7':
                mailing.sent_time = F('sent_time') + timedelta(days=7)
                mailing.mailing_status = 'launched'
            elif mailing.periodicity == '30':
                mailing.sent_time = F('sent_time') + timedelta(days=30)
                mailing.mailing_status = 'launched'
            mailing.save()

            try_status = 'success'
            server_response = 'успешно'
        except smtplib.SMTPResponseException as error:
            try_status = 'fail'
            server_response = str(error)

        finally:
            Logs.objects.create(mailing=mailing, try_status=try_status, server_response=server_response,
                                last_try_date=now)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        start_mailing,
        trigger=CronTrigger(minute="*/1"),
        id="start_mailing",
        max_instances=1,
        replace_existing=True,
    )
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...")
