from django.urls import path
from rest_framework import routers
from app.views import UserViewSet, ArticleViewSet, PhotoViewSet
from app import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'photos', PhotoViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.UserList.as_view(), name="users_list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="users_detail"),
    path("articles/", views.ArticleList.as_view(), name="articles_list"),
    path("articles/<int:pk>/", views.ArticleDetail.as_view(), name="articles_detail"),

    path("register/", views.register, name="register"),
    path("login/", views.log_in, name="login"), 
    path("logout/", views.log_out, name="logout")
]