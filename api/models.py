from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    prompt = models.TextField()
    response = models.TextField()
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)  # Ejemplo de archivo adjunto
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} by {self.user.username}"
