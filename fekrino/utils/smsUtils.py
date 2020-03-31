from fekrino.settings import SEND_SMS
from fekrino.celery import send_fekrino_sms_async, send_fectogram_sms_async


def send_sms(phone_number, token, pattern):
    if SEND_SMS:
        if pattern == 'fectogram':
            response = send_fectogram_sms_async.delay(phone_number=phone_number, token=token)
            return response
        elif pattern == 'fekrino':
            response = send_fekrino_sms_async.delay(phone_number=phone_number, token=token)
            return response