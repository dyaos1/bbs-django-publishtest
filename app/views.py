from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes

from app.models import User, Article, Photo
from rest_framework import viewsets, permissions, generics
from rest_framework.parsers import JSONParser
from app.serializers import UserSerializer, ArticleSerializer, PhotoSerializer

from app.permissions import IsOwnerOrReadOnly


# api view
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-joined_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().order_by('user_id')
    serializer_class = PhotoSerializer


# list view
def index(req):
    return HttpResponse("hello world")


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]


# Authentication
@csrf_exempt
@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def register(request):
    if request.method == 'POST':
        # data = JSONParser().parse(request)
        data = request.data
        username = data['username']
        raw_password = data['password']

        new_user = User.objects.create_user(
                username = username,
                password = raw_password
            )
        
        user = authenticate(request=request, username=username, password=raw_password)
        login(request, user)

        context = {
            "new_id": new_user.id,
            "new_username": new_user.username
        }

        return JsonResponse(context)

    else:
        return HttpResponse("register here")
    

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@csrf_exempt
def log_in(request):
    if request.method == "POST":
        username = request.data['username']
        raw_password = request.data['password']

        user = authenticate(username=username, password=raw_password)

        if user is not None:
            login(request, user)
        else:
            return HttpResponse("login failed")

        context = {
            "id": user.id,
            "username": user.username
        }

        return JsonResponse(context)

    return HttpResponse("loginview")


def log_out(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        username = request.user.username
        logout(request)
        return JsonResponse({
            "userid": user_id,
            "username": username,
            "status": "logged out"
        })
    else:
        return HttpResponse("nothing to logout")
