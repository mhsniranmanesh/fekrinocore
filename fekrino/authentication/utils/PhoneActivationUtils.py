from django.utils.crypto import get_random_string


def create_otp_token():
    return get_random_string(length=6, allowed_chars='123456789')