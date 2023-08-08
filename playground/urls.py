from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path(route='hello/', view=views.say_hello),
    path(route='hello-html/', view=views.say_hello_html, kwargs={'pk': None}, name='names') ,
    path(route='hello-html/<int:pk>', view=views.say_hello_html, name='name'),
    path(route='hello-html-rooms/', view=views.home, name='names'),
    path(route='hello-html-rooms/<int:pk>', view=views.room, name='name'),
]