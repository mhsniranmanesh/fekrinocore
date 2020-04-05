from django.utils.crypto import get_random_string


def create_user_random_password():
    return get_random_string(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                               'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                               '23456789')