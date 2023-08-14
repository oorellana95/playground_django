from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path(route='login/', view=views.loginPage, name="login"),
    path(route='logout/', view=views.logoutUser, name="logout"),
    path(route='register/', view=views.registerPage, name="register"),
    path(route='home/', view=views.home, name="home"),
    path(route='rooms/<int:pk>/', view=views.room, name="room"),
    path(route='create-room/', view=views.create_room, name="create-room"),
    path(route='update-room/<int:pk>', view=views.update_room, name="update-room"),
    path(route='delete-room/<int:pk>', view=views.delete_room, name="delete-room"),
    path(route='delete-message/<int:pk>', view=views.delete_message, name="delete-message")
]