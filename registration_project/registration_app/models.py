import email
from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20, null=True, blank=True)
    lastname = models.CharField(max_length=20, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
    
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
