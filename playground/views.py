from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request -> response
# request handler
# in some frameworks is called an action, in django is called views

def say_hello(request):
    return HttpResponse('Hello World')

def say_hello_html(request):
    return render(request=request, template_name='hello.html', context={'name':'Oscar'})

