from rest_framework import viewsets
from .models import *
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
        if(serializer.is_valid()):
            if(self.request.user in can_view_event(self.request.user)):
                serializer.save(uploader=self.request.user)
            else:
                raise PermissionDenied("You do not have permission to create a post for this event.")
       

class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    def get_queryset(self):
        user=self.request.user
        if(can_view_event(user)):
           return Reaction.objects.filter(post__in=Post.objects.filter(event__in=can_view_event(user)))

    def perform_create(self, serializer):
        if(serializer.is_valid()):
            if(self.request.user in can_view_event(self.request.user)):
                serializer.save(user=self.request.user)
            else:
                raise PermissionDenied("You do not have permission to react to this post.")


    