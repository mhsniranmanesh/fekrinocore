from datetime import datetime
from random import randint
from django.utils.crypto import get_random_string
from django.utils import timezone
from dateutil.relativedelta import relativedelta


def create_user_random_password():
    return get_random_string(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                                      'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                                      '23456789')


def generate_birthday_from_age(age):
    if age < 18:
        age = 18
    if age > 50:
        age = 50
    days_diff = randint(2, 10)
    months_diff = randint(1, 5)
    from_date = datetime.now()
    return from_date - relativedelta(years=age, months=months_diff, days=days_diff)


def generate_fake_phone_number():
    phone_number = '+98812' + get_random_string(length=7, allowed_chars='0123456789')
    return phone_number
