import uuid as uuid_lib
from django.contrib.gis.db import models
from django.utils import timezone

from fekrino.settings import MESSAGE_TYPE_CHOICES
from profiles.models.user import User


class Chat(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    self_user = models.ForeignKey(User, related_name='self_user_chats', on_delete=models.CASCADE)
    other_user = models.ForeignKey(User, related_name='other_user_chats', on_delete=models.CASCADE)

    def __str__(self):
        return "{0}-{1}".format(self.self_user.name, self.other_user.name)

    @property
    def chat_name(self):
        return str(self.uuid)


class Message(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    chat = models.ForeignKey(Chat, related_name='chat_messages', on_delete=models.CASCADE)
    type = models.IntegerField(default=1, choices=MESSAGE_TYPE_CHOICES)
    replied_to = models.OneToOneField('Message', null=True, blank=True, on_delete=models.SET_NULL)
    deleted_users = models.ManyToManyField(User, blank=True)
    sender = models.ForeignKey(User, related_name='sender_messages', on_delete=models.CASCADE)
    text = models.CharField(max_length=4096, null=True, blank=True)

    def __str__(self):
        return "{0} | {1} | {2}-{3} | {4}".format(self.type, self.sender, self.chat.self_user, self.chat.other_user,
                                                  self.text)
