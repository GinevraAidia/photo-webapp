from .models import *

def is_event_owner(user,event):
    return user == event.owner


def can_upload_to_event(user, event):
    if not user or not user.is_authenticated:
        return False
    return is_event_owner(user, event) or event.user.filter(id=user.id).exists()


