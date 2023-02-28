from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

# from django.contrib.auth.models import User
from base.models import Room, Topic, Message, User

# Serializes Python objects into JSON and vice versa

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username','name', 'email', 'bio']

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'