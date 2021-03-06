from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
user = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(user, related_name = 'author_messages', on_delete = models.CASCADE)
    content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def load():
        return Message.objects.order_by('-time_stamp').all().reverse()
    