from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# Create your views here

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics': topics} 
    return render(request=request, template_name='home.html', context=context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'rooms':[room]} 
    return render(request=request, template_name='home.html', context=context)

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

def update_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm(instance=room)
    context = {'form': form}
    return render(request, 'room_form.html', context)
    
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})