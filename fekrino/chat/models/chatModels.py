# from fekrino.db import models
# from profiles.models.user import User
#
#
# class Dialog(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user1', related_name='from_user',
#                               db_index=True)
#     opponent = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user2', related_name='to_user',
#                               db_index=True)
#     date_created = models.DateTimeField('date_created', auto_now_add=True, editable=False, db_index=True)
#
#     def __str__(self):
#         return _("Chat with ") + self.opponent.username
#
#
# class Message(models.Model):
#     dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, verbose_name='room',
#                                related_name='room_messages', db_index=True)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='recipient',
#                                related_name='message_sender', db_index=True)
#     read = models.BooleanField(verbose_name="read", default=False)
#     timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False, db_index=True)
#     body = models.TextField('body')
#
#     def __str__(self):
#         return self.sender.username + "(" + self.get_formatted_create_datetime() + ") - '" + self.text + "'"
#
#     def characters(self):
#         return len(self.body)
#
#     class Meta:
#         app_label = 'chat'
#         verbose_name = 'message'
#         verbose_name_plural = 'messages'
#         ordering = ('-timestamp',)
