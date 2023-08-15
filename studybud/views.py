from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Topic, Message, UserProfile
from .forms import RoomForm, UserForm, UserProfileForm

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = authenticate(request, username=username, password= password)
            if user is None:
                raise Exception("User or password does not exist")
            login(request, user)
            
            return redirect('home')
            
        except Exception as e:
            messages.error(request, e)

    context = {'page':page} 
    return render(request, 'login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    else:
        form = UserCreationForm()
    context = {'form':form} 
    return render(request, 'login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    q_topic = request.GET.get('q-topic') if request.GET.get('q-topic') != None else ''
    if q:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) | 
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
    elif q_topic:
        rooms = Room.objects.filter(Q(topic__name__icontains=q_topic)
        )
    else:
        rooms = Room.objects.all()
    topics = Topic.objects.all()[:5]
    total_rooms = Room.objects.count
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'topics': topics, 'total_rooms': total_rooms, 'rooms':rooms, 'room_messages': room_messages} 
    return render(request=request, template_name='home.html', context=context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        user = UserProfile.objects.get(user=request.user)
        Message.objects.create(
            user=user,
            room=room,
            body= request.POST.get('body')
        )
        room.participants.add(user)
        return redirect('room', pk=room.id)
    
    room_messages = room.message_set.all()
    participants = room.participants.all()
    context = {'room':room, 'room_messages': room_messages, 'participants':participants} 
    return render(request=request, template_name='room.html', context=context)

@login_required(login_url='/login')
def create_room(request):
    if request.method == 'POST':
        #request.POST.get('name')
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        user = UserProfile.objects.get(user=request.user)
        Room.objects.create(
            host=user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    else:
        form = RoomForm()

    topics = Topic.objects.all()
    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context)

@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host.user:
        return HttpResponse('You are not allowed to update this room!')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    else:
        form = RoomForm(instance=room)
    topics = Topic.objects.all()
    context = {'form': form, 'topics':topics, 'room': room}
    return render(request, 'room_form.html', context)

@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host.user:
        return HttpResponse('You are not allowed to delete this room!')
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    
    return render(request, 'delete.html', {'obj':room})

@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user not in (message.user.user, message.room.host.user):
        return HttpResponse('You are not allowed to delete this room!')
    
    if request.method == "POST":
        message.delete()
        return redirect('home')
    
    return render(request, 'delete.html', {'obj': message})

def user_profile(request, pk):
        user_profile = UserProfile.objects.get(id=pk)
        rooms = user_profile.room_set.all()
        room_messages = user_profile.message_set.all()
        total_rooms = Room.objects.count
        topics = Topic.objects.all()
        context = {'user_profile':user_profile, 'rooms': rooms, 'room_messages':room_messages, 'total_rooms':total_rooms, 'topics': topics}
        return render(request, 'profile.html', context)

@login_required(login_url='/login')
def update_user(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect('user-profile', pk=user.id)
    user_form = UserForm(instance=user)
    user_profile_form = UserProfileForm(instance=user_profile)
    context = {'user_form': user_form, 'user_profile_form': user_profile_form}
    return render(request, 'update_user.html', context)

def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    total_rooms = Room.objects.count
    context = {'topics': topics, 'total_rooms': total_rooms}
    return render(request, 'topics.html', context)

def activities(request):
    room_messages = Message.objects.all()
    context = {'topics': topics, 'room_messages': room_messages}
    return render(request, 'activity.html', context)