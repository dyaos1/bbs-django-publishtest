<<<<<<< Updated upstream
from django.shortcuts import render

# Create your views here.
=======
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import User, Article
from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser
from app.serializers import UserSerializer, ArticleSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-joined_at')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    # permission_classes = [permissions.IsAuthenticated]


# def TestView(req):
#     return HttpResponse("hi")


# detail view
@csrf_exempt
def article_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)
>>>>>>> Stashed changes
