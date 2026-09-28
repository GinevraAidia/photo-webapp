from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model= Event
        fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Reaction
        fields = '__all__'

class EventShareSerializer(serializers.ModelSerializer):
    class Meta:
        model= EventShare
        fields = '__all__'
