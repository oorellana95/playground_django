from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path(route='login/', view=views.login_page, name="login"),
    path(route='logout/', view=views.logout_user, name="logout"),
    path(route='register/', view=views.register_page, name="register"),
    path(route='update-user/', view=views.update_user, name="update-user"),
    path(route='home/', view=views.home, name="home"),
    path(route='rooms/<int:pk>/', view=views.room, name="room"),
    path(route='profile/<int:pk>/', view=views.user_profile, name="user-profile"),    
    path(route='create-room/', view=views.create_room, name="create-room"),
    path(route='update-room/<int:pk>', view=views.update_room, name="update-room"),
    path(route='delete-room/<int:pk>', view=views.delete_room, name="delete-room"),
    path(route='delete-message/<int:pk>', view=views.delete_message, name="delete-message")
]