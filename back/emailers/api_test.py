from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Member, EmailBurst
from .serializers import EmailBurstSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_emailer_api(request):
    """
    Test endpoint to verify the emailer functionality is working
    """
    try:
        # Check if we can import and use the emailer
        from utils.emailer import EmailSender, EmailStatus
        sender = EmailSender()
        
        # Return a success response
        return Response({
            'status': 'success',
            'message': 'Emailer utility is available and configured',
            'sender_email': sender.sender_email
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Emailer not configured: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_email_burst_stats(request, pk):
    """
    Get delivery statistics for a specific email burst
    """
    try:
        email_burst = EmailBurst.objects.get(pk=pk)
        return Response({
            'email_burst_id': email_burst.id,
            'total_recipients': email_burst.total_recipients,
            'sent_count': email_burst.sent_count,
            'failed_count': email_burst.failed_count,
            'success_rate': email_burst.success_rate
        })
    except EmailBurst.DoesNotExist:
        return Response({'error': 'EmailBurst not found'}, status=status.HTTP_404_NOT_FOUND)