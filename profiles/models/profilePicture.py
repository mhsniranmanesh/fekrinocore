import os
from django.db import models
import uuid as uuid_lib
from django.dispatch import receiver
from django.utils import timezone
from profiles.models.user import User


def profile_picture_attachment_path(instance):
    return 'profile_pictures/{0}/{1}.jpeg'.format(instance.user.uuid, instance.uuid)

def profile_picture_thumbnail_attachment_path(instance):
    return 'profile_pictures/{0}/{1}-avatar.jpeg'.format(instance.user.uuid, instance.uuid)


class ProfilePicture(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile_picture',
                                blank=True, null=True)
    profile_picture = models.ImageField(upload_to=profile_picture_attachment_path, blank=False)
    thumbnail = models.ImageField(upload_to=profile_picture_thumbnail_attachment_path, blank=False)
    priority = models.IntegerField(blank=False)


@receiver(models.signals.post_delete, sender=ProfilePicture)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=ProfilePicture)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = ProfilePicture.objects.get(pk=instance.pk).file
    except ProfilePicture.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
