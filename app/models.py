from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):    
   use_in_migrations = True

   def create_user(self, username, password):        
       if not username:            
           raise ValueError('must have username')
       if not password:            
           raise ValueError('must have user password')

       user = self.model(
           username = username
       )
       user.set_password(password)
       user.save(using=self._db)
       return user
   

class User(AbstractBaseUser):
    username = models.CharField(max_length=32)

    objects = UserManager()
#    is_active = models.BooleanField(default=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'


class Article(models.Model):
    title =  models.CharField(max_length=32)
    content =  models.CharField(max_length=32)
    author =  models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Photo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    photo_path = models.TextField(default = "default.png")
