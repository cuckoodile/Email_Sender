from django.contrib.auth.models import AbstractUser
from django.db import models
# from core.models import Member

# Create your models here.

class Member(AbstractUser):
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.get_full_name() if self.first_name and self.last_name else self.email
    
class EmailBurst(models.Model):
    sender = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    recipients = models.ManyToManyField(Member, related_name='received_email')

    def __str__(self):
        return f'{self.sender} {self.subject} {self.created_at}'