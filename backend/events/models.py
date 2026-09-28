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
    user=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='events_joined')
    def __str__(self):
        return f"title: {self.title} |description:{self.description} |visibility:{self.visibility} |username:{self.owner.username}"

class Post(models.Model):
    event=models.ForeignKey(Event, related_name='posts', on_delete=models.CASCADE)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    description = models.TextField(blank=True, default='')
    image=models.ImageField(upload_to='images/', blank=True, null=True)
    uploaded_at= models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"description: {self.description} |time uploaded:{self.uploaded_at:%d/%m/%Y %H:%M} |from:{self.uploader.username} |in event:{self.event}"

class Reaction(models.Model):
    post=models.ForeignKey(Post, related_name='reactions', on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reactions', on_delete=models.CASCADE)
    class emoji(models.TextChoices):
        LIKE="👍", "Like"
        DISLIKE="👎", "Dislike"
        HEART="❤️", "Heart"
        LAUGH="😂", "Laugh"
    emoji=models.CharField(max_length=255, choices=emoji.choices, default=emoji.LIKE)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'], 
                name='unique_user_reaction_per_post'
            )
        ]

    def __str__(self):
         return f"user:{self.user.username} |emoji:{self.emoji} |post:{self.post.description}"
