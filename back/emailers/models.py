from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum

# Create your models here.

class EmailDeliveryStatus(models.TextChoices):
    SENT = 'sent', 'Sent'
    FAILED = 'failed', 'Failed'
    NOT_FOUND = 'not_found', 'Not Found'
    CONNECTION_ERROR = 'connection_error', 'Connection Error'
    OTHER_ERROR = 'other_error', 'Other Error'


class MemberDeliveryStatus(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    email_burst = models.ForeignKey('EmailBurst', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=EmailDeliveryStatus.choices, default=EmailDeliveryStatus.SENT)
    error_message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'email_burst')  # Each member can have only one status per email burst


class Member(AbstractUser):
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name() if self.first_name and self.last_name else self.email


class EmailBurst(models.Model):
    sender = models.EmailField(max_length=254, blank=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='email_attachments/', null=True, blank=True)

    # Additional fields for tracking
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)

    recipients = models.ManyToManyField('Member', related_name='received_emails')

    def __str__(self):
        return f'{self.sender} - {self.subject[:50]} - {self.created_at}'

    @property
    def total_recipients(self):
        return self.recipients.count()

    @property
    def sent_count(self):
        return self.memberdeliverystatus_set.filter(status=EmailDeliveryStatus.SENT).count()

    @property
    def failed_count(self):
        return self.memberdeliverystatus_set.filter(
            status__in=[EmailDeliveryStatus.FAILED, EmailDeliveryStatus.NOT_FOUND,
                       EmailDeliveryStatus.CONNECTION_ERROR, EmailDeliveryStatus.OTHER_ERROR]
        ).count()

    @property
    def success_rate(self):
        total = self.total_recipients
        if total == 0:
            return 0
        return (self.sent_count / total) * 100
