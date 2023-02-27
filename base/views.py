from django.shortcuts import render, redirect
from django.http import HttpResponse

# from django.contrib.auth.models import User
from .models import Room, Topic, Message, User

from django.db.models import Q
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm, UserForm

def loginPage(request):
    if(request.user.is_authenticated):
        return redirect('home')

    if(request.method == 'POST'):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User with username: ' + username + ' does not exist!')
        
        user = authenticate(request, username=username, password=password)
        if(user is not None):
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password is incorrect!')

    context = {'page': 'login'}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if(request.method == 'POST'):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'ERROR: ocurred during registration!')

    context = {'form':form}
    return render(request, 'login_register.html', context)

def home(request):
    q = None
    if(request.GET.get('q') != None):
        q = request.GET.get('q')
    else:
        q = ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        # Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )
    topics = Topic.objects.all()[:4]

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[:4]
    all_rooms_count = Room.objects.all().count()

    context = {'rooms': rooms, 'topics': topics, 'room_messages': room_messages, 'all_rooms': all_rooms_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    # message_set -> give all children (Message) of the room
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()[0:4]
    topics = Topic.objects.all()[:4]
    all_rooms_count = Room.objects.all().count()

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics, 'all_rooms': all_rooms_count }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if(request.method == 'POST'):
        form = UserForm(request.POST, instance=user)
        if(form.is_valid()):
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form': form }
    return render(request, 'base/profile_edit.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if(request.method == 'POST'):
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )

        return redirect('home')

    topics = Topic.objects.all()
    context = {'form':form, 'topics': topics}
    return render(request, 'base/room_create_update.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if(request.user != room.host) :
        return HttpResponse('You are not allowed here! Its not your room')

    if(request.method == 'POST'):
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)

        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    topics = Topic.objects.all()  
    context = {'update': True, 'form': form, 'topics': topics, 'room': room }
    return render(request, 'base/room_create_update.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if(request.user != room.host) :
        return HttpResponse('You are not allowed to delete! Its not your room')

    if(request.method == 'POST'):
        room.delete()
        return  redirect('home')

    context = {'obj': room}
    return render(request, 'delete.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if(request.user != message.user) :
        return HttpResponse('You are not allowed to delete! Its not your message')

    if(request.method == 'POST'):
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'delete.html', context)

def topicsPage(request):
    q = None
    if(request.GET.get('q') != None):
        q = request.GET.get('q')
    else:
        q = ''

    topics = Topic.objects.filter(Q(name__icontains=q))
    all_rooms_count = Room.objects.all().count()
    context = {'topics': topics, 'all_rooms': all_rooms_count}
    return render(request, 'base/topics.html', context) 

def activitiesPage(request):
    room_messages = Message.objects.all()[:4]
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)