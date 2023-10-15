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
   
   def create_superuser(self, username, password):
       user = self.create_user(            
           username=username,                  
           password=password
       )
       user.is_admin = True
       user.is_superuser = True
       user.save(using=self._db)
       return user 
   

class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True)

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
    @property
    def is_staff(self):
        return self.is_admin

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Article(models.Model):
    title =  models.CharField(max_length=32)
    content =  models.CharField(max_length=32)
    author =  models.ForeignKey(User, related_name='article', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Photo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    photo_path = models.TextField(default = "default.png")
