from django.db import models
from django.contrib.auth.models import AbstractUser

class Member(AbstractUser):
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.get_full_name()