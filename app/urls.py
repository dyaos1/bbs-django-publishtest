from django.urls import path
from rest_framework import routers
from app.views import UserViewSet, ArticleViewSet, PhotoViewSet
from app import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView

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

    path("register/", views.RegisterAPIView.as_view()), # post - 회원가입
    path("auth/", views.AuthAPIView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()), # jwt 토큰 재발급

    path("upload/", views.UploadFile)

    # path("register/", views.register, name="register"),
    # path("login/", views.log_in, name="login"), 
    # path("logout/", views.log_out, name="logout")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)