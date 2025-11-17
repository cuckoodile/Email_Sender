from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *

# Member
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username', 'password', 'email', 'first_name', 'middle_name', 'last_name', 'is_verified', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = Member.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            middle_name=validated_data.get('middle_name'),
            last_name=validated_data.get('last_name'),
        )

        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance


# MemberDeliveryStatus
class MemberDeliveryStatusSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)

    class Meta:
        model = MemberDeliveryStatus
        fields = ['id', 'member', 'status', 'error_message', 'sent_at']


# EmailBurst
class EmailBurstSerializer(serializers.ModelSerializer):
    recipients = MemberSerializer(many=True, read_only=True)
    delivery_statuses = MemberDeliveryStatusSerializer(source='memberdeliverystatus_set', many=True, read_only=True)

    recipients_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Member.objects.all(),
        source='recipients',
        write_only=True
    )

    class Meta:
        model = EmailBurst
        fields = [
            'id', 'sender', 'subject', 'body', 'created_at', 'is_sent', 'sent_at', 'attachment',
            'recipients', 'recipients_ids', 'delivery_statuses',
            'total_recipients', 'sent_count', 'failed_count', 'success_rate'
        ]
        read_only_fields = ['created_at', 'is_sent', 'sent_at', 'total_recipients',
                           'sent_count', 'failed_count', 'success_rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make sender field optional so it can be auto-filled
        self.fields['sender'].required = False

    def validate(self, attrs):
        # If sender is not provided in the request, it will be auto-filled in the view
        # We allow it to be empty here, as it will be filled by the view
        return attrs
