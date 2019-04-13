import uuid as uuid_lib
from django.contrib.gis.db import models
from django.utils import timezone
from profiles.models.user import User


class Like(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    date = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(model=User, on_delete=models.CASCADE, related_name='user_likes')
    like = models.ForeignKey(model=User, on_delete=models.CASCADE, related_name='user_been_likes')


class Match(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    date = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(model=User, on_delete=models.CASCADE, related_name='user_unmatches')
    match = models.ForeignKey(model=User, on_delete=models.CASCADE, related_name='user_been_unmatches')


class UnMatch(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    date = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(model=User, on_delete=models.CASCADE, related_name='user_unmatches')
    unmatch = models.ForeignKey(model=User, on_delete=models.CASCADE, related_name='user_been_unmatches')