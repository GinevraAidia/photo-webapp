from django.db import transaction
from .permission import can_upload_to_event, can_view_post
from events.models import Event, Post, PostReaction, Reaction
from rest_framework.exceptions import PermissionDenied

class EventService:
    @staticmethod
    @transaction.atomic
    def create_event(*, owner, data):
        data = data.copy()
        users = data.pop("user", [])

        event = Event.objects.create(
            owner=owner,
            **data
        )
        event.user.set(users)

        return event

    @staticmethod
    @transaction.atomic
    def update_event(event, data, actor):

        for field, value in data.items():
            if field in ('user', 'users'):
                event.user.set(value)
            else:
                setattr(event, field, value)

        event.save()
        return event
    
    @staticmethod
    @transaction.atomic
    def delete_event(*,event,actor) -> None:
        if event.owner.id!=actor.id:
            raise PermissionDenied("You are not the owner of this event")
        event.delete()

class PostService: 
    @staticmethod
    @transaction.atomic
    def create_post(*, uploader, data):
        data = dict(data)
        event = data["event"]

        if not can_upload_to_event(uploader, event):
            raise PermissionDenied(
                "Non puoi pubblicare in questo evento."
            )

        return Post.objects.create(
            uploader=uploader,
            **data
        )

    @staticmethod
    @transaction.atomic
    def update_post(*, post, data, actor):
        if post.uploader_id != actor.id:
            raise PermissionDenied(
                "Non puoi modificare questo post."
            )

        # Non permettiamo di cambiare evento
        # durante la modifica del post
        data = dict(data)
        data.pop("event", None)

        for field, value in data.items():
            setattr(post, field, value)

        post.save()
        return post

    @staticmethod
    @transaction.atomic
    def delete_post(*, post, actor):
        if post.uploader_id != actor.id and post.event.owner_id != actor.id:
            raise PermissionDenied(
                "Non puoi eliminare questo post."
            )

        post.delete()

class PostReactionService:
    @staticmethod
    @transaction.atomic
    def set_reaction(*, post, user, reaction):

        if not can_view_post(user, post):
            raise PermissionDenied(
                "Non puoi reagire a questo post."
            )

        reaction, created = PostReaction.objects.update_or_create(
            post=post,
            user=user,
            defaults={"reaction": reaction}
        )

        return reaction, created

    @staticmethod
    @transaction.atomic
    def delete_reaction(*, reaction, actor):
        if reaction.user_id != actor.id:
            raise PermissionDenied(
                "Non puoi eliminare questa reazione."
            )

        reaction.delete()