from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=1024)
    
    created_at = models.DateTimeField(auto_now_add=True)

    photo_path = models.TextField(default = "default.png")


class Article(models.Model):
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=32)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class Photo(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     photo_path = models.TextField(default = "default.png")
