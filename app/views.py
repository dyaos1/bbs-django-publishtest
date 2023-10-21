import os
from uuid import uuid4
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, parser_classes
from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.response import Response

import jwt
import boto3

from app.models import User, Article, Photo
from app.serializers import UserSerializer, ArticleSerializer, PhotoSerializer
from app.permissions import IsOwnerOrReadOnly

from bbs.settings import MEDIA_ROOT, SECRET_KEY


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
    # permission_classes = [permissions.IsAuthenticated]
    

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().order_by('user_id')
    serializer_class = PhotoSerializer



class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # photo 
            Photo.objects.create(
                user = user, # 될지 몰랐는데 되더라. user object가 맞네
                photo_path = request.data['profile']
            )
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AuthAPIView(APIView):
    # 유저 정보 확인
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            print(request.COOKIES)
            access = request.COOKIES['access']
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
        print(request.data)
    	# 유저 인증
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response



# upload
@api_view(['POST'])
@csrf_exempt
def UploadFile(request):
    file = request.FILES.get('file')
    if file is not None:

        print(settings.AWS_BUCKET)

        # 로컬에 저장
        # uuid_name = uuid4().hex
        # save_path = os.path.join(MEDIA_ROOT, uuid_name)

        # with open(save_path, 'wb+') as destination:
        #     for chunk in file.chunks():
        #         destination.write(chunk)

        # S3 서비스
        try:
            file._set_name(str(uuid4()))
            s3 = S3ImgUploader(file)
            imgFile = s3.upload()
        except Exception as e:
            print(e)
            message = 'Failed s3'
            imgFile = "default.png"

        message = "uploaded fine"
    else:
        imgFile = 'default.png'
        message = "no upload"

    context = {
        "message": message,
        "uploadfile": imgFile
    }

    # print(context)
    return Response(context)
    




# boto3 imge uploader

class S3ImgUploader:
    def __init__(self, file):
        self.file = file

    def upload(self):
        print('===s3 upload start===')
        s3 = boto3.client(
            's3',
            aws_access_key_id     = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        )

        url = 'img'+'/'+uuid4().hex

        s3.upload_fileobj(self.file, 
                          settings.AWS_BUCKET,
                          url,
                          ExtraArgs={
                                "ContentType": self.file.content_type
                        })
        # content type 문제로 한참 오류가 났었음.

        print(url)

        return url




# dummy 화

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
