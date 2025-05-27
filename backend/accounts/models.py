import os
import shortuuid

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'webp')


def upload_to(instance, filename):
    ext = os.path.splitext(filename)[-1].lower()
    new_filename = shortuuid.uuid()[:8]

    return f'profiles/{str(instance.pk)[:8]}/{new_filename}{ext}'


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    
    email_verified = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    image = models.ImageField(
        upload_to=upload_to, null=True, blank=True,
        validators=[
            FileExtensionValidator(ALLOWED_EXTENSIONS)
        ]
    )

    display_name = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(max_length=300, null=True, blank=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if self._state.adding and not self.display_name:
            self.display_name = self.user.username

        super().save(*args, **kwargs)
