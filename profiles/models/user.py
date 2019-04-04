from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
import uuid as uuid_lib
from django.utils import timezone
from fekrino.utils.smsUtils import send_sms
from profiles.constants.userConstants import Constants
from profiles.utils.profilePictureUtils import random_string_generator
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=50,
        validators=[username_validator],
        help_text=_('Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )
    name = models.CharField(_('first name'), max_length=50, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=16,
        unique=True,
        db_index=True,
        blank=False
    )
    is_phone_number_verified = models.BooleanField(_('phone number verified'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    bio = models.CharField(_('biograghy'), max_length=3000, blank=True)
    job = models.CharField(_('job'), max_length=150, blank=True)
    university = models.CharField(_('university'), max_length=150, blank=True)
    balance = models.IntegerField(default=Constants.USER_INITIAL_BALANCE)
    rate = models.IntegerField(default=0)


    REQUIRED_FIELDS = ['phone_number', 'name']


    def send_token_sms(self, token):
        send_sms(self.phone_number, token)