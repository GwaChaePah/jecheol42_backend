from .models import Product, Post, Comment, OpenApi
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenApi
        fields = '__all__'
