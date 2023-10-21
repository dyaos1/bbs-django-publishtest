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
        fields = ['id', 'username', 'password'] # 혹시 노출되는거 아닌가 싶어서 password를 뺐더니 validate_data에서 빠지는 문제가 생겼음

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password']
        )
        return user


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
