from .models import Product, Post, Comment, OpenApi
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'image',
        ]


class BoardSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y.%m.%d %H:%M")
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'image1',
            'view_count',
            'created_at',
            'tag',
            'price',
            'user_key',
        ]


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y.%m.%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y.%m.%d %H:%M")
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y.%m.%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y.%m.%d %H:%M")
    class Meta:
        model = Comment
        fields = '__all__'


class PostDetailSerializer(serializers.Serializer):
    post = PostSerializer()
    comments = CommentSerializer(many=True)


class SearchSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y.%m.%d %H:%M")
    class Meta:
        model = OpenApi
        fields = '__all__'
