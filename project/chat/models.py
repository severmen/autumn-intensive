from datetime import datetime

from django.db import models

# Create your models here.
class Message(models.Model):

    nikname = models.CharField(max_length=150)
    data_time = models.DateTimeField( default=datetime.now)
    message = models.CharField(max_length=400)

    class Meta:
        ordering = ['-data_time']

    def __str__(self):
        return self.message