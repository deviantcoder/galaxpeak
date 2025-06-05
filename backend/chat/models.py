import shortuuid

from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()


class Chat(models.Model):
    class ChatType(models.TextChoices):
        PRIVATE = ('private', 'Private')
        GROUP = ('group', 'Group')

    chat_type = models.CharField(max_length=10, choices=ChatType.choices)
    name = models.CharField(max_length=100, null=True, blank=True)
    members = models.ManyToManyField(User, related_name='chats', through='ChatMembership')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = shortuuid.uuid()
        super().save(*args, **kwargs)
        

class ChatMembership(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('chat', 'user')


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    
    def __str__(self):
        return f'[{self.created.strftime("%Y-%m-%d %H:%M:%S")}] {self.sender}: {self.content[:30]}'
