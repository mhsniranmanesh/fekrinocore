from django.contrib.gis.db import models
from profiles.models.user import User


class Contact(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username


class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)



# class Dialog(TimeStampedModel):
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"), related_name="selfDialogs",
#                               on_delete=models.CASCADE)
#     opponent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog opponent"), on_delete=models.CASCADE)
#
#     def __str__(self):
#         return _("Chat with ") + self.opponent.username
#
#
# class Message(TimeStampedModel, SoftDeletableModel):
#     dialog = models.ForeignKey(Dialog, verbose_name=_("Dialog"), related_name="messages", on_delete=models.CASCADE)
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="messages",
#                                on_delete=models.CASCADE)
#     text = models.TextField(verbose_name=_("Message text"))
#     read = models.BooleanField(verbose_name=_("Read"), default=False)
#     all_objects = models.Manager()
#
#     def get_formatted_create_datetime(self):
#         return dj_date(localtime(self.created), settings.DATETIME_FORMAT)
#
#     def __str__(self):
#         return self.sender.username + "(" + self.get_formatted_create_datetime() + ") - '" + self.text + "'"















# class Message(models.Model):
#     """
#     A private directmessage
#     """
#     content = models.TextField(_('Content'))
#     sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_dm', verbose_name=_("Sender"))
#     recipient = models.ForeignKey(AUTH_USER_MODEL, related_name='received_dm', verbose_name=_("Recipient"))
#     sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
#     read_at = models.DateTimeField(_("read at"), null=True, blank=True)
#
#     @property
#     def unread(self):
#         """returns whether the message was read or not"""
#         if self.read_at is not None:
#             return False
#         return True
#
#     def __str__(self):
#         return self.content
#
#     def save(self, **kwargs):
#         if self.sender == self.recipient:
#             raise ValidationError("You can't send messages to yourself")
#
#         if not self.id:
#             self.sent_at = timezone.now()
#         super(Message, self).save(**kwargs)















# class PMManager(models.Manager):
#
#     def sent(self, user):
#         """Limit to PMs sent by <user>"""
#
#         return self.get_queryset().filter(
#                 sender=user,
#                 sender_deleted=False)
#
#     def archived(self, user):
#         """Limit to PMs received and archived by <user>"""
#
#         return self.get_queryset().filter(
#                 recipient=user,
#                 recipient_deleted=False,
#                 recipient_archived=True
#                 )
#
#     def received(self, user):
#         """Limit to PMs received by <user>"""
#
#         return self.get_queryset().filter(
#                 recipient=user,
#                 recipient_archived=False,
#                 recipient_deleted=False
#                 )
# @python_2_unicode_compatible
# class PM(AbstractText):
#     subject = models.CharField(max_length=64, blank=True, default='')
#     sent = models.DateTimeField(default=tznow, editable=False)
#     sender = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='pms_sent',
#     )
#     sender_deleted = models.BooleanField(default=False)
#     recipient = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='pms_received',
#     )
#     recipient_archived = models.BooleanField(default=False)
#     recipient_deleted = models.BooleanField(default=False)
#
#     objects = PMManager()
#
#     #assert False, 'tii'
#
#     class Meta:
#         db_table = 'nano_privmsg_pm'
#
#     def __str__(self):
#         if self.subject:
#             return self.subject
#         else:
#             return self.text[:64]
#
#     def save(self, *args, **kwargs):
#         if not self.subject:
#             snippet = self.text[:64]
#             ls = len(snippet)
#             if ls == 64 and ls < len(self.text):
#                 snippet = snippet[:-1] + '…'
#             self.subject = snippet
#         super(PM, self).save(*args, **kwargs)
#
#     def delete(self):
#         if self.is_deleted():
#             super(PM, self).delete()
#
# #     @models.permalink
# #     def get_absolute_url(self):
# #         return ('show_pms', (), {'msgid': self.id, 'uid':}
# #         )
#
#     def is_deleted(self):
#         if self.sender_deleted and self.recipient_deleted:
#             return True
#         if (self.sender_deleted or self.recipient_deleted) and self.sender == self.recipient:
#             return True
#         return False














# @python_2_unicode_compatible
# class Message(models.Model):
#     title = models.SlugField(primary_key=True, verbose_name=_("title"))
#     content = models.TextField(max_length=65536, blank=True, null=True, verbose_name=_("content"))
#     level = models.SmallIntegerField(default=settings.DEFAULT_MESSAGE_LEVEL,
#         choices=settings.MESSAGE_LEVELS.items(), verbose_name=_("level"))
#     template_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("template name"))
#     read_by = models.ManyToManyField(django_settings.AUTH_USER_MODEL, blank=True, verbose_name=_("read by"),
#         help_text=_("Users who read this message"))
#
#     class Meta:
#         app_label = 'volatile_messages'
#         verbose_name = _("message")
#         verbose_name_plural = _("messages")
#
#     def __str__(self):
#         return self.title
#
#     @property
#     def tag(self):
#         return self.get_level_display()
#
#     @property
#     def is_template(self):
#         return not bool(self.content)
#
#     def get_content(self):
#         if self.content:
#             return self.content
#         template_names = ['volatile_messages/%s.html' % self.title]
#         try:
#             return select_template(template_names).render({
#                 'message': self,
#             })
#         except TemplateDoesNotExist:
#             return _("No content, please update the message or create a template.")
#
#     def get_preview(self):
#         content = self.get_content()
#         preview = defaultfilters.truncatechars_html(content, 300)
#         return mark_safe(preview)
#     get_preview.short_description = _("Preview")
#
#     def is_read_by(self, user):
#         return self.read_by.filter(id=user.id).exists()
#
#     def read(self, user):
#         self.read_by.add(user)











# class MessageManager(models.Manager):
#
#     def inbox_for(self, user):
#         """
#         Returns all messages that were received by the given user and are not
#         marked as deleted.
#         """
#         return self.filter(
#             recipient=user,
#             recipient_deleted_at__isnull=True,
#         )
#
#     def outbox_for(self, user):
#         """
#         Returns all messages that were sent by the given user and are not
#         marked as deleted.
#         """
#         return self.filter(
#             sender=user,
#             sender_deleted_at__isnull=True,
#         )
#
#     def trash_for(self, user):
#         """
#         Returns all messages that were either received or sent by the given
#         user and are marked as deleted.
#         """
#         return self.filter(
#             recipient=user,
#             recipient_deleted_at__isnull=False,
#         ) | self.filter(
#             sender=user,
#             sender_deleted_at__isnull=False,
#         )
#
#
# @python_2_unicode_compatible
# class Message(models.Model):
#     """
#     A private message from user to user
#     """
#     subject = models.CharField(_("Subject"), max_length=140)
#     body = models.TextField(_("Body"))
#     sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_messages', verbose_name=_("Sender"), on_delete=models.PROTECT)
#     recipient = models.ForeignKey(AUTH_USER_MODEL, related_name='received_messages', null=True, blank=True, verbose_name=_("Recipient"), on_delete=models.SET_NULL)
#     parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True, verbose_name=_("Parent message"), on_delete=models.SET_NULL)
#     sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
#     read_at = models.DateTimeField(_("read at"), null=True, blank=True)
#     replied_at = models.DateTimeField(_("replied at"), null=True, blank=True)
#     sender_deleted_at = models.DateTimeField(_("Sender deleted at"), null=True, blank=True)
#     recipient_deleted_at = models.DateTimeField(_("Recipient deleted at"), null=True, blank=True)
#
#     objects = MessageManager()
#
#     def new(self):
#         """returns whether the recipient has read the message or not"""
#         if self.read_at is not None:
#             return False
#         return True
#
#     def replied(self):
#         """returns whether the recipient has written a reply to this message"""
#         if self.replied_at is not None:
#             return True
#         return False
#
#     def __str__(self):
#         return self.subject
#
#     def get_absolute_url(self):
#         return reverse('messages_detail', args=[self.id])
#
#     def save(self, **kwargs):
#         if not self.id:
#             self.sent_at = timezone.now()
#         super(Message, self).save(**kwargs)
#
#     class Meta:
#         ordering = ['-sent_at']
#         verbose_name = _("Message")
#         verbose_name_plural = _("Messages")
#
#
# def inbox_count_for(user):
#     """
#     returns the number of unread messages for the given user but does not
#     mark them seen
#     """
#     return Message.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True).count()
#
# # fallback for email notification if django-notification could not be found
# if "pinax.notifications" not in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
#     from django_messages.utils import new_message_email
#     signals.post_save.connect(new_message_email, sender=Message)








