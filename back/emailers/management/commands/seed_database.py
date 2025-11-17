from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from emailers.models import Member, EmailBurst
from django.utils import timezone
from datetime import datetime, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample data: 2 staff users, 10 dummy members, and 2 emails'

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')
        
        # Create 2 staff users
        staff_data = [
            {
                'username': 'staff_john',
                'email': 'john.doe@staff.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'password123'
            },
            {
                'username': 'staff_jane',
                'email': 'jane.smith@staff.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'password': 'password123'
            }
        ]
        
        staff_users = []
        for staff_info in staff_data:
            staff, created = User.objects.get_or_create(
                username=staff_info['username'],
                defaults={
                    'email': staff_info['email'],
                    'first_name': staff_info['first_name'],
                    'last_name': staff_info['last_name'],
                    'is_staff': True,
                    'is_active': True
                }
            )
            if created:
                staff.set_password(staff_info['password'])
                staff.save()
                self.stdout.write(f"Created staff user: {staff.username}")
            else:
                self.stdout.write(f"Staff user already exists: {staff.username}")
            staff_users.append(staff)
        
        # Create 10 dummy members
        member_data = [
            {'username': 'member1', 'email': 'member1@example.com', 'first_name': 'Alice', 'last_name': 'Johnson', 'middle_name': 'Marie'},
            {'username': 'member2', 'email': 'member2@example.com', 'first_name': 'Bob', 'last_name': 'Williams', 'middle_name': 'James'},
            {'username': 'member3', 'email': 'member3@example.com', 'first_name': 'Carol', 'last_name': 'Brown', 'middle_name': 'Ann'},
            {'username': 'member4', 'email': 'member4@example.com', 'first_name': 'David', 'last_name': 'Jones', 'middle_name': 'Robert'},
            {'username': 'member5', 'email': 'member5@example.com', 'first_name': 'Emma', 'last_name': 'Garcia', 'middle_name': 'Louise'},
            {'username': 'member6', 'email': 'member6@example.com', 'first_name': 'Frank', 'last_name': 'Miller', 'middle_name': 'Thomas'},
            {'username': 'member7', 'email': 'member7@example.com', 'first_name': 'Grace', 'last_name': 'Davis', 'middle_name': 'Elizabeth'},
            {'username': 'member8', 'email': 'member8@example.com', 'first_name': 'Henry', 'last_name': 'Rodriguez', 'middle_name': 'Michael'},
            {'username': 'member9', 'email': 'member9@example.com', 'first_name': 'Ivy', 'last_name': 'Martinez', 'middle_name': 'Rose'},
            {'username': 'member10', 'email': 'member10@example.com', 'first_name': 'Jack', 'last_name': 'Hernandez', 'middle_name': 'Lee'}
        ]
        
        members = []
        for member_info in member_data:
            member, created = Member.objects.get_or_create(
                username=member_info['username'],
                defaults={
                    'email': member_info['email'],
                    'first_name': member_info['first_name'],
                    'last_name': member_info['last_name'],
                    'middle_name': member_info['middle_name'],
                    'is_active': True
                }
            )
            if created:
                member.set_password('password123')
                member.save()
                self.stdout.write(f"Created member: {member.username}")
            else:
                self.stdout.write(f"Member already exists: {member.username}")
            members.append(member)
        
        # Create 2 email bursts
        email_data = [
            {
                'subject': 'Welcome to Our Community!',
                'body': '''
                <h1>Welcome to Our Community!</h1>
                <p>Dear Member,</p>
                <p>We are excited to have you join our community. You'll find that we offer the best services and support to help you achieve your goals.</p>
                <p>Best regards,<br>The Team</p>
                ''',
                'sender': staff_users[0].email
            },
            {
                'subject': 'Monthly Newsletter - October 2024',
                'body': '''
                <h1>Monthly Newsletter - October 2024</h1>
                <p>Dear Members,</p>
                <p>Here's what's happening this month:</p>
                <ul>
                    <li>New features added to our platform</li>
                    <li>Upcoming events and webinars</li>
                    <li>Tips and best practices</li>
                </ul>
                <p>Stay tuned for more updates!</p>
                <p>Best regards,<br>The Team</p>
                ''',
                'sender': staff_users[1].email
            }
        ]
        
        for i, email_info in enumerate(email_data):
            email_burst, created = EmailBurst.objects.get_or_create(
                subject=email_info['subject'],
                defaults={
                    'body': email_info['body'],
                    'sender': email_info['sender']
                }
            )
            if created:
                # Add some members as recipients (first email gets first 5 members, second gets last 5)
                start_idx = i * 5
                end_idx = start_idx + 5
                selected_members = members[start_idx:end_idx]
                email_burst.recipients.set(selected_members)
                self.stdout.write(f"Created email burst: {email_burst.subject}")
            else:
                self.stdout.write(f"Email burst already exists: {email_burst.subject}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded the database!\n'
                f'- Created {len(staff_users)} staff users\n'
                f'- Created {len(members)} members\n'
                f'- Created {len(email_data)} email bursts'
            )
        )