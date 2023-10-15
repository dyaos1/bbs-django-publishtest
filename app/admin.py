from django.contrib import admin
from app.models import User, Article, Photo

# Register your models here.

admin.site.register(User)
admin.site.register(Article)
admin.site.register(Photo)