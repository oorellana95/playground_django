from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# Create your views here

def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms} 
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
