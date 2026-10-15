from django.db import models
from django.conf import settings
# Create your models here.


class Event(models.Model):
    class Visibility(models.TextChoices):
            PRIVATE="private", "Private"
            PUBLIC="public", "Public"
    visibility=models.CharField(max_length=255, choices=Visibility.choices, default=Visibility.PRIVATE) 
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='events', on_delete=models.CASCADE)
    title= models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    user=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='events_joined',blank=True)
    def __str__(self):
        return f"TITLE: {self.title} | DESCRIPTION: {self.description} | VISIBILITY: {self.visibility} | USERNAME: {self.owner.username}"

class Post(models.Model):
    event=models.ForeignKey(Event, related_name='posts', on_delete=models.CASCADE)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    description = models.TextField(blank=True, default='')
    image=models.ImageField(upload_to='images/', blank=True, null=True)
    uploaded_at= models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"DESCRIPTION: {self.description} | FROM: {self.uploader.username} | IN EVENT: {self.event.id}"

class Reaction(models.Model):
    name=models.CharField(max_length=50,unique=True)
    symbol=models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - {self.symbol}"
    
class PostReaction(models.Model):
     post=models.ForeignKey(Post, related_name='post_reactions', on_delete=models.CASCADE)
     user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='post_reactions', on_delete=models.CASCADE)
     reaction=models.ForeignKey(Reaction, related_name='post_reactions', on_delete=models.PROTECT)
     class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'], 
                name='unique_user_reaction_per_post'
            )
        ]
        def __str__(self):
            return f"{self.user} - {self.reaction} - {self.post_id}"
