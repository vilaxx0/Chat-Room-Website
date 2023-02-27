from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Topic, Message, User

from .serializers import RoomsSerializer

# URL:          /api/
# Description:  Shows all routes in the API
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/',

        'GET /api/rooms/',
        'GET /api/rooms/<str:pk>/',
        'POST /api/rooms/create/',
        'POST /api/rooms/<str:pk>/update/',
        'DELETE /api/rooms/<str:pk>/delete/',

        'GET /api/rooms/<str:pk>/messages/',
        'POST /api/rooms/<str:pk>/messages/create/',
        'DELETE /api/rooms/<str:pk>/messages/<str:pk>/delete/',

        'GET /api/rooms/<str:pk>/participants/',
    ]
    # return JsonResponse(routes, safe=False)
    return Response(routes)
    
# URL:          /api/rooms/
# Description:  Shows all rooms
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomsSerializer(rooms, many=True)
    return Response(serializer.data)

# URL:          /api/rooms/<str:pk>/
# Description:  Shows a specific room
@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomsSerializer(room, many=False)
    return Response(serializer.data)