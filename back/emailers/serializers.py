from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import *

# Member
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'username', 'password', 'email', 'first_name', 'middle_name', 'last_name', 'is_verified']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = Member.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            email=validated_data.get('email'),
            first_name=validated_data.get('username'),
            middle_name=validated_data.get('middle_name'),
            last_name=validated_data.get('username'),
        )

        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance
    

# EmailBurst
class EmailBurstSerializer(serializers.ModelSerializer):
    recipients = MemberSerializer(many=True, read_only=True)
    
    recipients_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Member.objects.all(),
        source='recipients',
        write_only=True
    )

    class Meta:
        model = EmailBurst
        fields = [
            'id', 'sender', 'subject', 'body', 'created_at',
            'recipients',
            'recipients_ids'
        ]
        read_only_fields = ['created_at']