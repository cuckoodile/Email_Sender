from django.core.management.base import BaseCommand
from emailers.tasks import send_email_burst_task
from emailers.models import EmailBurst
import sys


class Command(BaseCommand):
    help = 'Test sending an email burst by ID'

    def add_arguments(self, parser):
        parser.add_argument('email_burst_id', type=int, help='ID of the EmailBurst to send')
    
    def handle(self, *args, **options):
        email_burst_id = options['email_burst_id']
        
        try:
            email_burst = EmailBurst.objects.get(pk=email_burst_id)
        except EmailBurst.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'EmailBurst with ID {email_burst_id} does not exist')
            )
            sys.exit(1)
        
        # Check if email has already been sent
        if email_burst.is_sent:
            self.stdout.write(
                self.style.WARNING(f'EmailBurst with ID {email_burst_id} has already been sent')
            )
            sys.exit(1)
        
        self.stdout.write(
            self.style.NOTICE(f'Queuing email burst {email_burst_id} for sending...')
        )
        
        # Queue the email sending task
        result = send_email_burst_task.delay(email_burst_id)
        
        self.stdout.write(
            self.style.SUCCESS(f'Task queued successfully with ID: {result.task_id}')
        )
        self.stdout.write(
            self.style.SUCCESS('Make sure Celery worker is running to process the task')
        )