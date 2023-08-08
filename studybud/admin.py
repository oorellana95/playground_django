from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message
admin.site.register(Room) #used to interact with the table in the admin panel
admin.site.register(Topic)
admin.site.register(Message)