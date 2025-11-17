from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

from .models import *
from .serializers import *
from .tasks import send_email_burst_task, send_scheduled_email_burst_task

# Import test API views
from .api_test import test_emailer_api, get_email_burst_stats

# Create your views here.

# EmailBurst

class EmailBurstListCreateAPIView(ListCreateAPIView):
    queryset = EmailBurst.objects.all().order_by('-created_at')
    serializer_class = EmailBurstSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Get the recipients from the request data
        recipients_data = self.request.data.get('recipients', [])

        # Auto-fill the sender field with the logged-in user's email
        user = self.request.user
        if user.is_authenticated and not self.request.data.get('sender'):
            email_burst = serializer.save(sender=user.email)
        else:
            email_burst = serializer.save()

        # Handle the many-to-many relationship for recipients
        if recipients_data:
            # If recipients_data is a string (JSON from frontend), parse it
            if isinstance(recipients_data, str):
                import json
                recipients_list = json.loads(recipients_data)
            else:
                recipients_list = recipients_data

            # Query the Member objects by email
            recipient_emails = [email for email in recipients_list if isinstance(email, str)]
            recipients = Member.objects.filter(email__in=recipient_emails)

            # Set the recipients
            email_burst.recipients.set(recipients)

        # Note: Email sending is triggered separately via the send_email_burst endpoint
        # This keeps the creation endpoint fast and reliable

class EmailBurstRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EmailBurst.objects.all()
    serializer_class = EmailBurstSerializer
    permission_classes = [IsAuthenticated]


# Custom view to send email burst asynchronously
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email_burst(request, pk):
    """
    Send the email burst asynchronously to all recipients and track delivery status
    """
    try:
        email_burst = EmailBurst.objects.get(pk=pk)
    except EmailBurst.DoesNotExist:
        return Response({'error': 'EmailBurst not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if email has already been sent
    if email_burst.is_sent:
        return Response({'error': 'EmailBurst has already been sent'}, status=status.HTTP_400_BAD_REQUEST)

    # Get all recipients
    recipients = email_burst.recipients.all()
    if not recipients:
        return Response({'error': 'No recipients found'}, status=status.HTTP_400_BAD_REQUEST)

    # Queue the email sending task
    task = send_email_burst_task.delay(email_burst.id)

    # Return immediate response
    return Response({
        'email_burst_id': email_burst.id,
        'message': 'Email sending task has been queued',
        'task_id': task.task_id,
        'total_recipients': len(recipients)
    }, status=status.HTTP_200_OK)


# Custom view to schedule email burst
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_email_burst(request, pk):
    """
    Schedule the email burst to be sent at a specific time
    """
    try:
        email_burst = EmailBurst.objects.get(pk=pk)
    except EmailBurst.DoesNotExist:
        return Response({'error': 'EmailBurst not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if email has already been sent
    if email_burst.is_sent:
        return Response({'error': 'EmailBurst has already been sent'}, status=status.HTTP_400_BAD_REQUEST)

    # Get scheduled time from request
    scheduled_time = request.data.get('scheduled_time')
    if not scheduled_time:
        return Response({'error': 'Scheduled time is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Parse the scheduled time
    try:
        scheduled_datetime = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
    except ValueError:
        return Response({'error': 'Invalid datetime format'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a periodic task that runs once at the scheduled time
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.SECONDS,
    )

    task = PeriodicTask.objects.create(
        interval=schedule,
        name=f'Scheduled Email Burst {email_burst.id} - {scheduled_datetime}',
        task='emailers.tasks.send_scheduled_email_burst_task',
        args=json.dumps([email_burst.id]),
        start_time=scheduled_datetime,
        one_off=True  # Run only once
    )

    return Response({
        'email_burst_id': email_burst.id,
        'message': 'Email scheduled successfully',
        'task_id': task.id,
        'scheduled_time': scheduled_datetime.isoformat()
    }, status=status.HTTP_200_OK)


# Members
class MemberListCreateAPIView(ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


# Staff-specific views
class StaffListAPIView(ListCreateAPIView):
    queryset = Member.objects.filter(is_staff=True)
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Member.objects.filter(is_staff=True)


class StaffRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.filter(is_staff=True)
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Member.objects.filter(is_staff=True)


# Non-Staff (Member) views
class NonStaffListAPIView(ListCreateAPIView):
    queryset = Member.objects.filter(is_staff=False)
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Member.objects.filter(is_staff=False)


class NonStaffRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.filter(is_staff=False)
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Member.objects.filter(is_staff=False)
