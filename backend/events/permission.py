from django.db.models import Q
from .models import *
from rest_framework.exceptions import PermissionDenied


def can_upload_to_event(user, event):
    if not user or not user.is_authenticated:
        return False
    return (Q(owner=user) or Q(event.user.filter(id=user.id).exists())).distinct()

def can_view_event(user):
    if user.is_anonymous:
        raise PermissionDenied("You must be logged in to view events.") 
    return Event.objects.filter(Q(visibility="public") | Q(owner=user) | Q(user=user)).distinct()
