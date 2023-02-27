from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from django.contrib.auth.models import User
from base.models import Room, Topic, Message

# Serializes Python objects into JSON and vice versa

class RoomsSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'