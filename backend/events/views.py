from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

class EventShareViewSet(viewsets.ModelViewSet):
    queryset = EventShare.objects.all()
    serializer_class = EventShareSerializer
