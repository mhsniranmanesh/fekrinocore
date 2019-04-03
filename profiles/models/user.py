from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    def user_profile_picture_path(self, filename):
        random_string = random_string_generator(size=5)
        final_file_name = ''.join([self.username, random_string])
        return 'profile_pictures/{0}.jpeg'.format(final_file_name)

    def user_avatar_path(self, filename):
        random_string = random_string_generator(size=5)
        final_file_name = ''.join([self.username, random_string])
        return 'profile_pictures/{0}-avatar.jpeg'.format(final_file_name)

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
    phone_number = models.CharField(_('phone number'), max_length=16, blank=True)
    is_email_verified = models.BooleanField(_('email verified'), default=False)
    is_freelancer = models.BooleanField(_('is user freelancer'), db_index=True, default=False, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    title = models.CharField(_('title'), max_length=150, blank=True)
    bio = models.CharField(_('biograghy'), max_length=3000, blank=True)
    job = models.CharField(_('job'), max_length=150, blank=True)
    degree = models.CharField(_('degree'), max_length=150, blank=True)
    university = models.CharField(_('university'), max_length=150, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True)
    wish_coins = models.IntegerField(default=Constants.USER_INITIAL_WISHCOINS)
    balance = models.IntegerField(default=Constants.USER_INITIAL_BALANCE)
    client_rate = models.IntegerField(default=0)
    freelancer_rate = models.IntegerField(default=0)
    client_score = models.IntegerField(default=0)
    freelancer_score = models.IntegerField(default=0)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


