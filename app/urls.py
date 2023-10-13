from rest_framework import routers
from app.views import UserViewSet, ArticleViewSet, PhotoViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'photos', PhotoViewSet)

urlpatterns = [
]