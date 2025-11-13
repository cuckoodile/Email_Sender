from django.db import models
from core.models import Member

# Create your models here.

class EmailBurst(models.Model):
    sender = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    body = models.TextField()

    recipients = models.ManyToManyField("app.Model", related_name='received_email')