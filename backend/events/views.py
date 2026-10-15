from xml.dom import ValidationErr

from django.contrib.admin import action
from rest_framework import viewsets,permissions
from rest_framework import status
from rest_framework.response import Response
from events.services import UserService,EventService, PostService, PostReactionService
from events.models import *
from .serializers import *
from .permission import *
from django.contrib.auth import get_user_model
User=get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch","get"]
    def get_object(self):
        return self.request.user
    def perform_update(self, serializer):
        user = UserService.update_user(
            user=self.request.user,
            data=serializer.validated_data,
            actor=self.request.user
        )
        serializer.instance = user

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return can_view_event(self.request.user).select_related("owner").prefetch_related("user")

    def perform_create(self, serializer):
        event = EventService.create_event(
        owner=self.request.user,
        data=serializer.validated_data
        )

        serializer.instance = event

    def perform_update(self, serializer):
        event= EventService.update_event(
            event=self.get_object(),
            data=serializer.validated_data,
            actor=self.request.user
        )
        serializer.instance=event
        
    def perform_destroy(self, instance):
        EventService.delete_event(event=instance,actor=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,isPostOwnerOrEventOwner]
    
    def get_queryset(self):
        queryset = Post.objects.filter(event__in=can_view_event(self.request.user)).select_related("event","uploader")
        event_id = self.request.query_params.get('event')
        if self.action=="list":
            if not event_id:
                raise ValidationErr("Event ID is required for listing posts.")
            queryset = queryset.filter(event_id=event_id)
        return queryset
    
    def perform_create(self, serializer):
        post = PostService.create_post( #fare i controlli qua sui permessi
            uploader=self.request.user,
            data=serializer.validated_data
        )
        serializer.instance = post

    def perform_update(self, serializer):
        post = PostService.update_post(
            post=self.get_object(),
            data=serializer.validated_data,
            actor=self.request.user
        )
        serializer.instance = post

    def perform_destroy(self, instance):
        PostService.delete_post(
            post=instance,
            actor=self.request.user
        )
        
class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all().order_by("id")
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

class PostReactionViewSet(viewsets.ModelViewSet):
    serializer_class = PostReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    http_method_names=["get","post","delete","head","options"]
    def get_queryset(self):
        queryset = PostReaction.objects.filter(
            post__event__in=can_view_event(
                self.request.user
            )
        ).select_related("user", "post__event")

        post_id = self.request.query_params.get("post")

        if post_id:
            queryset = queryset.filter(post_id=post_id)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = serializer.validated_data["post"]
        reaction_type = serializer.validated_data["reaction"]

        post_reaction, created = PostReactionService.set_reaction(
            post=post,
            user=request.user,
            reaction=reaction_type
        )

        output = self.get_serializer(post_reaction)

        return Response(
            output.data,
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )

    def perform_destroy(self, instance):
        PostReactionService.delete_reaction(
            reaction=instance,
            actor=self.request.user
        )

    