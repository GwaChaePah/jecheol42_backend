from .models import Product, Post, OpenApi
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


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenApi
        fields = '__all__'
