from django.core.management.base import BaseCommand
from emailers.models import Member, EmailBurst
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create sample data for testing the emailer system'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Create sample members
        if not Member.objects.filter(email='member1@example.com').exists():
            member1 = Member.objects.create_user(
                username='member1',
                email='member1@example.com',
                password='password123',
                first_name='John',
                last_name='Doe'
            )
            self.stdout.write(self.style.SUCCESS(f'Created user: {member1.username}'))
        
        if not Member.objects.filter(email='member2@example.com').exists():
            member2 = Member.objects.create_user(
                username='member2',
                email='member2@example.com',
                password='password123',
                first_name='Jane',
                last_name='Smith'
            )
            self.stdout.write(self.style.SUCCESS(f'Created user: {member2.username}'))
        
        # Create a sample email burst
        if not EmailBurst.objects.filter(subject='Welcome to our service!').exists():
            email_burst = EmailBurst.objects.create(
                sender='noreply@yourcompany.com',
                subject='Welcome to our service!',
                body='<h1>Welcome!</h1><p>Thank you for joining us.</p>'
            )
            
            # Add members as recipients
            member1 = Member.objects.get(email='member1@example.com')
            member2 = Member.objects.get(email='member2@example.com')
            email_burst.recipients.add(member1, member2)
            
            self.stdout.write(self.style.SUCCESS(f'Created email burst: {email_burst.subject}'))
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data for testing')
        )