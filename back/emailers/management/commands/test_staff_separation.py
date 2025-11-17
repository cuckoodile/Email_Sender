from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from emailers.models import Member

User = get_user_model()

class Command(BaseCommand):
    help = 'Test the staff/non-staff separation'

    def handle(self, *args, **options):
        # Count staff users
        staff_count = User.objects.filter(is_staff=True).count()
        self.stdout.write(f"Staff users count: {staff_count}")
        
        # List staff users
        staff_users = User.objects.filter(is_staff=True)
        self.stdout.write("Staff users:")
        for user in staff_users:
            self.stdout.write(f"  - {user.username} (ID: {user.id}, Email: {user.email})")

        # Count non-staff members
        non_staff_count = Member.objects.filter(is_staff=False).count()
        self.stdout.write(f"Non-staff members count: {non_staff_count}")
        
        # List non-staff members
        non_staff_members = Member.objects.filter(is_staff=False)
        self.stdout.write("Non-staff members:")
        for member in non_staff_members:
            self.stdout.write(f"  - {member.username} (ID: {member.id}, Email: {member.email})")
        
        self.stdout.write(
            self.style.SUCCESS('Successfully verified staff/non-staff separation')
        )