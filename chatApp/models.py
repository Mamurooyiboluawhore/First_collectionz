from django.db import models
from accounts.models import *

# Create your models here.
class ChatMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user' )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender' )
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever' )
    messasge = models.CharField(max_length=700,)
    is_read =models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
     
    class Meta:
        ordering = ['-created_at']  # Message shown in descending order by default
        verbose_name_plural = 'Messages'

        def __str__(self) -> str:
            return f"Message from {self.sender} to {self.reciever}"
        