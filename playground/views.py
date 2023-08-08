from django.shortcuts import render
from django.http import HttpResponse
from studybud.models import Room

# Create your views here.
# request -> response
# request handler
# in some frameworks is called an action, in django is called views

def say_hello(request):
    return HttpResponse('Hello World')

names = [
    {'id':  1, 'name': 'Oscar'},
    {'id':  2, 'surname': 'Orellana'},
    {'id':  3, 'name': 'Montse'},
]
def say_hello_html(request, pk):
    if pk:
        context = {'names': [name for name in names if name.get('id') == pk]}
    else:
        context = {'names':names} 
    return render(request=request, template_name='hello.html', context=context)

def home(request):
    rooms = Room.objects.all()
    context = {'names':rooms} 
    return render(request=request, template_name='hello.html', context=context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'names':[room]} 
    return render(request=request, template_name='hello.html', context=context)