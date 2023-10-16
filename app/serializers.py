from app.models import User, Article, Photo
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'joined_at']

#     # def create(self, validated_data):
#     #     return User.objects.create(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    # article = serializers.PrimaryKeyRelatedField(many=True, queryset=Article.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Article
        fields = ['id', 'url', 'title', 'content', 'author', 'created_at', 'updated_at']
        # fields = '__all__'

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Article` instance, given the validated data.
    #     """
    #     return Article.objects.create(**validated_data)


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Photo
        fields = '__all__'
