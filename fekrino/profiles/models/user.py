from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
import uuid as uuid_lib
from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from fekrino.fekrino.utils.smsUtils import send_sms
from fekrino.profiles.constants.userConstants import Constants


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Man'),
        ('W', 'Woman'),
    )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=50,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(_('name'), max_length=50, blank=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), max_length=50, unique=True)
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
        db_index=True,
        blank=False
    )
    is_phone_number_verified = models.BooleanField(_('phone number verified'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    bio = models.CharField(_('biograghy'), max_length=3000, blank=True)
    work = models.CharField(_('work'), max_length=150, blank=True)
    university = models.CharField(_('university'), max_length=150, blank=True)
    balance = models.IntegerField(default=Constants.USER_INITIAL_BALANCE)
    rate = models.IntegerField(default=0)
    location = models.PointField(null=True)
    gender = models.CharField(blank=True, choices=GENDER_CHOICES, max_length=10)

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'name']
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    def send_token_sms(self, token):
        send_sms(self.phone_number, token)