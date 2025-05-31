from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import uuid


class ChatSession(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, editable=False)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    def __str__(self):
        return f"ChatSession {self.uuid} by {self.user}"

class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, db_index=True)
    ROLE_CHOICES = [
        ('user', 'User'),
        ('system', 'System'),
        ('assistant', 'Assistant'),
        ('tool', 'Tool'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, editable=False)
    content = models.TextField(editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    tool_calls = models.JSONField(default=dict)

    def __str__(self):
        return f"Message: {self.content}"

    class Meta:
        ordering = ['timestamp']
