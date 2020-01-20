from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class User(models.Model):

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = "用户"
        verbose_name_plural = "用户"

