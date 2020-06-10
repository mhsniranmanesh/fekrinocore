import uuid as uuid_lib
from django.contrib.gis.db import models
from django.utils import timezone
from profiles.models.user import User


class Like(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    like = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_been_likes')

    def __str__(self):
        return "{0} ---> {1}".format(self.user, self.like)


class SuperLike(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_super_likes')
    superlike = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_been_super_likes')

    def __str__(self):
        return "{0} ---> {1}".format(self.user, self.superlike)


class Dislike(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_dislikes')
    dislike = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_been_dislikes')

    def __str__(self):
        return "{0} ---> {1}".format(self.user, self.dislike)


class Match(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_matches')
    match = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_been_matches')

    def __str__(self):
        return "{0} ---> {1}".format(self.user, self.match)


class UnMatch(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_unmatches')
    unmatch = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_been_unmatches')

    def __str__(self):
        return "{0} ---> {1}".format(self.user, self.unmatch)