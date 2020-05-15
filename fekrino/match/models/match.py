import uuid as uuid_lib
from django.contrib.gis.db import models
from django.utils import timezone
from profiles.models.user import User


class Like(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    like = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_been_likes')


class SuperLike(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_super_likes')
    superlike = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_been_super_likes')


class Dislike(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_dislikes')
    dislike = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_been_dislikes')


class Match(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_matches')
    match = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_been_matches')


class UnMatch(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_unmatches')
    unmatch = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_been_unmatches')