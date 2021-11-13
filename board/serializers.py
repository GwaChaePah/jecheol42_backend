from .models import Product, Post, Comment, OpenApi
from rest_framework import serializers
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'image',
        ]
        read_only_fields = [
            'id',
            'name',
            'image',
            'month',
        ]


class BoardSerializer(serializers.ModelSerializer):
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
        read_only_fields = [
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
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = [
            'id',
            'view_count',
            'created_at',
            'updated_at',
            'user_key',
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'post_key',
            'user_key',
        ]


class PostDetailSerializer(serializers.Serializer):
    post = PostSerializer()
    comments = CommentSerializer(many=True)


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenApi
        fields = '__all__'
        read_only_fields = [
            'item_name',
            'kind_name',
            'rank',
            'unit',
            'date',
            'price',
            'average_price',
            'created_at',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
        ]
