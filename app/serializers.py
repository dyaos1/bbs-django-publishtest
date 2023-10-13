from app.models import User, Article, Photo
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'joined_at']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only = True)
    class Meta:
        model = Article
        # fields = ['title', 'content', 'author', 'created_at', 'updated_at']
        fields = '__all__'


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Photo
        fields = '__all__'