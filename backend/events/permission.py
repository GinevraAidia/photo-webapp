from django.db.models import Q
from .models import *
from rest_framework.exceptions import PermissionDenied
from django.db.models import QuerySet
from rest_framework import permissions

def can_upload_to_event(user, event) -> bool:
    if not user or not user.is_authenticated:
        raise PermissionDenied("You must be logged in to upload to events.")
    return event.owner_id == user.id or event.user.filter(id=user.id).exists() or event.visibility == "public"

def can_view_post(user, post):
    if not user or not user.is_authenticated:
        return False

    return can_view_event(user).filter(
        pk=post.event_id
    ).exists()

def can_view_event(user) -> QuerySet[Event]:
    if user.is_anonymous:
        raise PermissionDenied("You must be logged in to view events.") 
    return Event.objects.filter(Q(visibility="public") | Q(owner=user) | Q(user=user)).distinct()

""" class IsOwnerOrReadOnly(permissions.BasePermission):
    
    Tutti possono vedere (GET/HEAD/OPTIONS),
    ma solo il proprietario può modificare o eliminare (PUT/PATCH/DELETE).
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if not request.user or not request.user.is_authenticated:
            return False

        obj_owner = getattr(obj, 'owner', None) or getattr(obj, 'uploader', None) or getattr(obj, 'user', None)

        return obj_owner == request.user """

class isPostOwnerOrEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ("PUT", "PATCH"):
            return obj.uploader == request.user
        if request.method == "DELETE":
            return obj.uploader == request.user or obj.event.owner == request.user
        return False