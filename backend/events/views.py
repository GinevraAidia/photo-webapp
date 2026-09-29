from rest_framework import viewsets

from events.services import EventService
from events.models import *
from .serializers import *
from .permission import *

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    def get_queryset(self):
            user = self.request.user
            return can_view_event(user)

    
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    def get_queryset(self):
         user=self.request.user
         if(can_view_event(user)):
            return Post.objects.filter(event__in=can_view_event(user)).distinct()
         
    def perform_create(self, serializer):
        event: Event = serializer.validated_data["event"]
        if not can_upload_to_event(self.request.user, event):
            raise PermissionDenied("You do not have permission to create a post for this event.")
        EventService.save(event)
        

class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    def get_queryset(self):
        user=self.request.user
        if(can_view_event(user)):
           return Reaction.objects.filter(post__in=Post.objects.filter(event__in=can_view_event(user)))

    def perform_create(self, serializer):
        post: Post = serializer.validated_data["post"]
        user = self.request.user
        if not can_upload_to_event(self.request.user, post.event):
            raise PermissionDenied("You do not have permission to react to this post.")
        serializer.save(user=self.request.user)


    