from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path(route='home/', view=views.home, name="home"),
    path(route='rooms/<int:pk>/', view=views.room, name="rooms"),
]