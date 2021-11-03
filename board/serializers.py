from .models import Product, Post
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'month']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'image1',
            'image2',
            'image3',
            'view_count',
            'created_at',
            'updated_at',
            'tag',
            'price',
            'user_key'
        ]
