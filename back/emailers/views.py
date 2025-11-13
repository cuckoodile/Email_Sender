from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import *
from .serializers import *
# Create your views here.

# EmailBurst
class EmailBurstListCreateAPIView(ListCreateAPIView):
    queryset = EmailBurst.objects.all()
    serializer_class = EmailBurstSerializer

class EmailBurstRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = EmailBurst.objects.all()
    serializer_class = EmailBurstSerializer


# Members
class MemberListCreateAPIView(ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class MemberRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

