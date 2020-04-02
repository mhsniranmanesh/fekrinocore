import os
import uuid as uuid_lib

from django.contrib.gis.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string

from profiles.models.user import User


def profile_picture_attachment_path(instance, filename):
    filename = get_random_string(length=5, allowed_chars='123456789')
    return 'profile_pictures/{0}/img-{1}.jpeg'.format(instance.user.uuid, filename)


def profile_picture_thumbnail_attachment_path(instance, filename):
    filename = get_random_string(length=5, allowed_chars='123456789')
    return 'profile_pictures/{0}/thumb-{1}.jpeg'.format(instance.user.uuid, filename)


class ProfilePicture(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False)
    date_created = models.DateTimeField(default=timezone.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_pictures',
                                blank=True, null=True)
    image = models.ImageField(upload_to=profile_picture_attachment_path, blank=False)
    thumbnail = models.ImageField(upload_to=profile_picture_thumbnail_attachment_path, blank=False)
    priority = models.IntegerField(blank=False)


@receiver(models.signals.post_delete, sender=ProfilePicture)
def auto_delete_image_and_thumbnail_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)

    return False


@receiver(models.signals.pre_save, sender=ProfilePicture)
def auto_delete_image_and_thumbnail_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        profile_picture = ProfilePicture.objects.get(pk=instance.pk)
        old_image = profile_picture.image
        old_thumbnail = profile_picture.thumbnail

        if old_image:
            new_image = instance.image

            if not old_image == new_image:
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)

        if old_thumbnail:
            new_thumbnail = instance.thumbnail

            if not old_thumbnail == new_thumbnail:
                if os.path.isfile(old_thumbnail.path):
                    os.remove(old_thumbnail.path)

        return False
    except User.DoesNotExist:
        return False
