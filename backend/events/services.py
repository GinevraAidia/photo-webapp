from django.db import transaction
from events.models import Event


class EventService:
    @staticmethod
    @transaction.atomic
    def create_event(data: dict) -> Event:

        event = Event.objects.create(**data)
        return event

    @staticmethod
    @transaction.atomic
    def save(event: Event):
        event.save()

    @staticmethod
    @transaction.atomic
    def update_event(event_id: int, data: dict) -> Event:
        event = Event.objects.get(id=event_id)
        for key, value in data.items():
            setattr(event, key, value)
        event.save()
        return event

    @staticmethod
    @transaction.atomic
    def delete_event(event_id: int) -> None:
        event = Event.objects.get(id=event_id)
        event.delete()
