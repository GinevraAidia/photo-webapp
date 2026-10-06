from rest_framework import viewsets,permissions
from rest_framework import status
from rest_framework.response import Response
from events.services import EventService
from events.models import *
from .serializers import *
from .permission import *
from django.contrib.auth import get_user_model
from django.views.generic.edit import DeleteView
User=get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
            user = self.request.user
            return can_view_event(user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" class EventDeleteView(DeleteView):
    def dispatch(self, request):
        if is_event_owner(request.user, self.get_object()):
           return super().dispatch(request)
        raise PermissionDenied("Solo il proprietario può eliminare questo evento.")
     """
    
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        user=self.request.user

        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return Post.objects.all()

        evento_id = self.request.query_params.get('event')
        if not evento_id:
            return Post.objects.none()
        return Post.objects.filter(
            event__in=can_view_event(user),
            event_id=evento_id
        ).distinct()
    
    def perform_create(self, serializer):
        event: Event = serializer.validated_data["event"]
        if not can_upload_to_event(self.request.user, event):
            raise PermissionDenied("You do not have permission to create a post for this event.")
        EventService.save(event)
        serializer.save(uploader=self.request.user)
        

class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    def get_queryset(self):
        user=self.request.user
        qs = Reaction.objects.filter(post__in=Post.objects.filter(event__in=can_view_event(user)))
        post_id = self.request.query_params.get('post')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def create(self, request):

        post_id = request.data.get('post')
        user = self.request.user
        if not post_id:
            return Response({"post": ["Questo campo è obbligatorio."]}, status=status.HTTP_400_BAD_REQUEST)

        existing_reaction = Reaction.objects.filter(post_id=post_id, user=user).first()

        if existing_reaction:
            #PATCH
            serializer = self.get_serializer(existing_reaction, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            if not can_upload_to_event(user, existing_reaction.post.event):
                raise PermissionDenied("You do not have permission to react to this post.")
                
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        #POST
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        post = serializer.validated_data["post"]
        if not can_upload_to_event(user, post.event):
            raise PermissionDenied("You do not have permission to react to this post.")
            
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    