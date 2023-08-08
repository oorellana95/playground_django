from django.shortcuts import render
from .models import Room
# Create your views here

def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms} 
    return render(request=request, template_name='home.html', context=context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'rooms':[room]} 
    return render(request=request, template_name='home.html', context=context)