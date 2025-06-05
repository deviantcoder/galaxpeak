import os
import shutil

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Profile


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
        )


@receiver(post_delete, sender=Profile)
def delete_profile_media_files(sender, instance, **kwargs):
    try:
        path = os.path.join(settings.MEDIA_ROOT, 'profiles', str(instance.pk)[:8])
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        pass
