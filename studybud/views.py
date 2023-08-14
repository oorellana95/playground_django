from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room, Topic
from .forms import RoomForm

def loginPage(request):
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

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):

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
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms, 'topics': topics, 'room_count': room_count} 
    return render(request=request, template_name='home.html', context=context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'rooms':[room]} 
    return render(request=request, template_name='home.html', context=context)

@login_required(login_url='/login')
def create_room(request):
    if request.method == 'POST':
        #request.POST.get('name')
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm()
    context = {'form': form}
    return render(request, 'room_form.html', context)

@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.user:
        return HttpResponse('You are not allowed to update this room!')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm(instance=room)
    context = {'form': form}
    return render(request, 'room_form.html', context)

@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.user:
        return HttpResponse('You are not allowed to delete this room!')
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})