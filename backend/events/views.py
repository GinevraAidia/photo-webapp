from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from .models import *
from .serializers import *
from .permission import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .permission import *

class EventViewSet(viewsets.ModelViewSet):
    #queryset = Event.objects.all()
    serializer_class = EventSerializer
    def get_queryset(self):
            user = self.request.user
            if user.is_anonymous:
                raise PermissionDenied("You must be logged in to view events.") 
            return Event.objects.filter(Q(visibility="public") | Q(owner=user))
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer


    