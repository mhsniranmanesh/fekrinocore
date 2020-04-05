from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from django.core.mail import EmailMultiAlternatives
from kavenegar import KavenegarAPI

from fekrino.fekrino.settings import KAVENEGAR_API_KEY

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fekrino.settings')

app = Celery('fekrino')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    # 'update-map-blocks': {
    #     'task': 'locations.tasks.update_map_blocks',
    #     'schedule': crontab(hour='*/2'),
    # },
    # 'update_complete_map': {
    #     'task': 'locations.tasks.update_complete_map',
    #     'schedule': crontab(minute='*/15', hour='*'),
    # },
    # 'backup-database': {
    #     'task': 'celery.tasks.backup_database',
    #     'schedule': crontab(minute=0, hour=0),
    # },
}
#
# app.conf.task_default_queue = 'default'
# app.conf.task_queue_max_priority = 10
# app.conf.task_queues = (
#     Queue('default',
#           routing_key='task.#'
#           ),
#     Queue('backup_tasks',
#           routing_key='backup.#',
#           queue_arguments={'x-max-priority': 1}
#           ),
#     Queue('single_email_tasks',
#           routing_key='mail.#',
#           queue_arguments={'x-max-priority': 3}
#           ),
#     Queue('mass_email_tasks',
#           routing_key='mass-mail.#',
#           queue_arguments={'x-max-priority': 2}
#           ),
# )
#
# task_default_exchange = 'tasks'
# task_default_exchange_type = 'topic'
# task_default_routing_key = 'task.default'
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(3, test.s('hello'))
#     sender.add_periodic_task(7, test.s('world'))


@app.task(bind=True, default_retry_delay=10)
def send_mail_async(self, subject, from_email, to_email, text_content, html_content):
    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as exc:
        self.retry(exc=exc)


# @app.task(bind=True, default_retry_delay=10)
# def send_sms_async(self, phone_number, token):
#     try:
#         sms = ghasedak.Ghasedak(GHASEDAK_API_KEY)
#         params = {
#             'receptor': phone_number,
#             'template': 'otp',
#             'type': 1,
#             "param1": token
#         }
#         result = sms.verification(params)
#         if not result:
#             self.retry()
#     except Exception as exc:
#         self.retry(exc=exc)


@app.task(bind=True, default_retry_delay=10)
def send_fekrino_sms_async(self, phone_number, token):
    try:
        api = KavenegarAPI(KAVENEGAR_API_KEY)
        params = {
            'receptor': phone_number,
            'template': 'fekrino',
            'token': token,
            'type': 'sms',
        }
        api.verify_lookup(params)
    except Exception as exc:
        self.retry(exc=exc)


@app.task(bind=True, default_retry_delay=10)
def send_fectogram_sms_async(self, phone_number, token):
    try:
        api = KavenegarAPI(KAVENEGAR_API_KEY)
        params = {
            'receptor': phone_number,
            'template': 'fectogram',
            'token': token,
            'type': 'sms',
        }
        api.verify_lookup(params)
    except Exception as exc:
        self.retry(exc=exc)


@app.task()
def backup_database():
    pass
    #os.system('pg_dump -h wishworkstage.ir -p 7799 wishworkcore > /home/moh3en_ir/backups/wish_work.back')

