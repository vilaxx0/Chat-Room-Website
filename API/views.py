from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import Room, Topic, Message, User

from .serializers import RoomSerializer, TopicSerializer, MessageSerializer, UserSerializer

# Method:       GET
# URL:          /api/
# Description:  Shows all routes in the API
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/',
        'GET POST /api/topics/',
        'GET POST /api/rooms/',
        'GET PUT DELETE /api/rooms/<id>/',
        'GET /api/rooms/<id>/participants/',
        'GET /api/rooms/<id>/messages/',
    ]
    return Response(routes)

# Method:       GET and POST
# URL:          /api/topics
# Description:  Shows all topics/Creates a new topic
@api_view(['GET', 'POST'])
def getCreateTopics(request):
    if request.method == 'GET':
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)
    
    if(request.method == 'POST'):
        serializer = TopicSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Method:       GET and POST
# URL:          /api/rooms/
# Description:  Shows all rooms/Creates a new room
@api_view(['GET', 'POST'])
def getCreateRooms(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    
    if(request.method == 'POST'):
        serializer = RoomSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# URL:          /api/rooms/<id>/
# Description:  Shows a specific room by id/Updates a room/Deletes a room
@api_view(['GET', 'PUT', 'DELETE'])
def getUpdateDeleteRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if(request.method == 'GET'):
        serializer = RoomSerializer(room, many=False)
        return Response(serializer.data)
    
    if(request.method == 'PUT'):
        serializer = RoomSerializer(instance=room, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if(request.method == 'DELETE'):
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# URL:          /api/rooms/<id>/participants/
# Description:  Shows all participants in a room
@api_view(['GET'])
def getParticipants(request, pk):
    room = Room.objects.get(id=pk)
    participants = room.participants.all()
    serializer = UserSerializer(participants, many=True)
    return Response(serializer.data)

# URL:          /api/rooms/<id>/messages/
# Description:  Shows all messages in a room by id
@api_view(['GET'])
def getMessages(request, pk):
    messages = Message.objects.filter(room=pk)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)