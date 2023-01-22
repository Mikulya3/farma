import send as send
from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from applications.spam.models import Spam
from applications.spam.serializers import SpamSerializer


class SpamAPIView(ModelViewSet):
    queryset = Spam.objects.all()
    serializer_class = SpamSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    success_url = '/'
    template_name = 'main/spam.html'


