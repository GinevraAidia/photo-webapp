from django.db.models import Q
from .models import *
from rest_framework.exceptions import PermissionDenied
from django.db.models import QuerySet

def can_upload_to_event(user, event) -> bool:
    if not user or not user.is_authenticated:
        raise PermissionDenied("You must be logged in to upload to events.")
    return event.owner_id == user.id or event.user.filter(id=user.id).exists()


def can_view_event(user) -> QuerySet[Event]:
    if user.is_anonymous:
        raise PermissionDenied("You must be logged in to view events.") 
    return Event.objects.filter(Q(visibility="public") | Q(owner=user) | Q(user=user)).distinct()
