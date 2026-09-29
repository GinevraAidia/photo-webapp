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
        event = serializer.validated_data["event"]
        if not can_upload_to_event(self.request.user, event):
            raise PermissionDenied("You do not have permission to create a post for this event.")
        serializer.save(uploader=self.request.user)
        

class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    def get_queryset(self):
        user=self.request.user
        if(can_view_event(user)):
           return Reaction.objects.filter(post__in=Post.objects.filter(event__in=can_view_event(user)))

    def perform_create(self, serializer):
        post: Post = serializer.validated_data["post"]
        user = self.request.user
        #prendo l'elenco di tutti gli eventi che quel utente può vedere, e poi con filter guardo se tra quelli c'è
        #quello con id della reaction passata  (exist è perchè voglio solo saper se esiste o no non voglio l'oggetto di return)
        if not can_view_event(user).filter(id=post.event_id).exists():
            raise PermissionDenied("You do not have permission to react to this post.")

        serializer.save(user=user)


    