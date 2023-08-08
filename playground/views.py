from django.shortcuts import render
from django.http import HttpResponse

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
def say_hello_html(request):
    context = {'names':names}
    return render(request=request, template_name='hello.html', context=context)

