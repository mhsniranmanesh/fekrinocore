from django.contrib.gis.db import models
from django.utils import timezone
import uuid as uuid_lib


class PhoneActivationToken(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)
    token = models.CharField(max_length=16, blank=False)
    phone_number = models.CharField(max_length=16, db_index=True, blank=False)
    is_last = models.BooleanField(default=False)
    is_again = models.BooleanField(default=False)