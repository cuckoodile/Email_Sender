from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from emailers.models import Member, EmailBurst

User = get_user_model()

class Command(BaseCommand):
    help = 'Display the seeded data'

    def handle(self, *args, **options):
        # Count staff users
        staff_count = User.objects.filter(is_staff=True).count()
        self.stdout.write(f"Staff users: {staff_count}")
        
        # List staff users
        staff_users = User.objects.filter(is_staff=True)
        for user in staff_users:
            self.stdout.write(f"  - {user.username} ({user.email})")
        
        # Count members
        member_count = Member.objects.count()
        self.stdout.write(f"Members: {member_count}")
        
        # List members
        members = Member.objects.all()
        for member in members:
            self.stdout.write(f"  - {member.username} ({member.email})")
        
        # Count email bursts
        email_count = EmailBurst.objects.count()
        self.stdout.write(f"Email bursts: {email_count}")
        
        # List email bursts
        email_bursts = EmailBurst.objects.all()
        for email in email_bursts:
            recipient_count = email.recipients.count()
            self.stdout.write(f"  - {email.subject} (to {recipient_count} members)")
        
        self.stdout.write(
            self.style.SUCCESS('Successfully displayed seeded data')
        )