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

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatsessions')
    model_code = models.CharField(max_length=255, default='Llama-3.1-8B-Instruct')
    created_at = models.DateTimeField(auto_now_add=True)

class ConversationMessage(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=[('system','system'),('user','user'),('assistant','assistant')])
    content = models.TextField()
    type = models.CharField(max_length=20, default='text') # 'text' o 'code'
    timestamp = models.DateTimeField(auto_now_add=True)