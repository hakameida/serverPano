from rest_framework import serializers
from django.conf import settings
from apiPano.models import Post, PostImage
from apiPano.models import CustomUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_admin']
class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()  # Handles file uploads directly

    class Meta:
        model = PostImage
        fields = ['id', 'image', 'caption']

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True,read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'images']

