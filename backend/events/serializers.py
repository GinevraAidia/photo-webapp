from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email']
        read_only_fields = ['id']

class PostSerializer(serializers.ModelSerializer):
    username_utente = serializers.SerializerMethodField()
    class Meta:
        model= Post
        fields = ['id','event','username_utente','description','image']

    def get_username_utente(self, obj):
        if obj.uploader:
            return obj.uploader.username
        return None

class EventSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), source='user'
    )

    class Meta:
        model= Event
        # fields = '__all__'
        fields=['id','owner','title','description','visibility','users']

class ReactionSerializer(serializers.ModelSerializer):
    username_utente = serializers.SerializerMethodField()
    class Meta:
        model= Reaction
        fields = ['post','emoji','username_utente']
        
    def get_username_utente(self, obj):
        if obj.user:
            return obj.user.username
        return None
        

