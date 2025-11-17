from celery import shared_task
from django.utils import timezone
from .models import EmailBurst, MemberDeliveryStatus
from utils.emailer import EmailSender, EmailStatus


@shared_task
def send_email_burst_task(email_burst_id):
    """
    Asynchronous task to send email burst to all recipients and track delivery status
    """
    try:
        email_burst = EmailBurst.objects.get(pk=email_burst_id)
    except EmailBurst.DoesNotExist:
        return {'error': 'EmailBurst not found'}

    # Check if email has already been sent
    if email_burst.is_sent:
        return {'error': 'EmailBurst has already been sent'}

    # Get all recipients
    recipients = email_burst.recipients.all()
    if not recipients:
        return {'error': 'No recipients found'}

    # Initialize email sender
    try:
        email_sender = EmailSender()
    except ValueError as e:
        return {'error': str(e)}

    # Send emails to all recipients
    failed_emails = []
    successful_emails = []

    for recipient in recipients:
        # Determine whether to include attachment
        attachment_path = None
        if email_burst.attachment:
            try:
                attachment_path = email_burst.attachment.path
            except ValueError:
                # If the file path is not accessible, skip the attachment
                attachment_path = None

        result = email_sender.send_single_email(
            receiver_email=recipient.email,
            subject=email_burst.subject,
            html_content=email_burst.body,
            attachment_path=attachment_path
        )

        # Create delivery status record
        status_obj = MemberDeliveryStatus.objects.create(
            member=recipient,
            email_burst=email_burst,
            status=result['status'].value,
            error_message=result.get('message', '')
        )

        if result['status'] == EmailStatus.SENT:
            successful_emails.append(recipient.email)
        else:
            failed_emails.append({
                'email': recipient.email,
                'error': result.get('message', 'Unknown error')
            })

    # Update email burst status
    email_burst.is_sent = True
    email_burst.sent_at = timezone.now()
    email_burst.save()

    # Return summary
    return {
        'email_burst_id': email_burst.id,
        'total_recipients': len(recipients),
        'successful_emails': len(successful_emails),
        'failed_emails': len(failed_emails),
        'success_rate': email_burst.success_rate,
        'failed_details': failed_emails
    }


@shared_task
def send_scheduled_email_burst_task(email_burst_id):
    """
    Task to send a scheduled email burst at a specific time
    """
    return send_email_burst_task(email_burst_id)