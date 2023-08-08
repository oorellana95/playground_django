from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    
class Room (models.Model):
    # the id is generated authomatically, 1-2-3...
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # when the room is deleted we still mantain the rooms
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants = 
    updated = models.DateTimeField(auto_now=True) #updates the timestamp for every change
    created = models.DateTimeField(auto_now_add=True) #only takes the timestamp when we create the instance

    class Meta:
        ordering = ['-updated', '-created'] # the negative in front means reverse

    def __str__(self) -> str:
        return self.name
    
class Message(models.Model):
    #user model is authomatically created by django
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 

    def __str__(self) -> str:
        return self.body[0:50]