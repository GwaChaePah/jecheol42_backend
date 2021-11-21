from .models import Product, Post, Comment, OpenApi, Profile, Region
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
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
    comment_cnt = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_comment_cnt(self, obj):
        pk = obj.id
        queryset = Comment.objects.filter(post_key=pk)
        comment_cnt = len(queryset)
        return comment_cnt

    def get_username(self, obj):
        user = obj.user_key
        username = user.username
        return username

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
            'username',
            'comment_cnt',
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
            'username',
            'comment_cnt',
        ]


class PostSerializer(serializers.ModelSerializer):
    comment_cnt = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_comment_cnt(self, obj):
        pk = obj.id
        queryset = Comment.objects.filter(post_key=pk)
        comment_cnt = len(queryset)
        return comment_cnt

    def get_username(self, obj):
        user = obj.user_key
        username = user.username
        return username

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = [
            'id',
            'view_count',
            'created_at',
            'updated_at',
            'user_key',
            'username',
            'comment_cnt',
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        user = obj.user_key
        username = user.username
        return username

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'post_key',
            'user_key',
            'username'
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


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
            'pk',
            'username',
        ]
        read_only_fields = [
            'pk'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'region'
        ]


class UserInfoSerializer(serializers.ModelSerializer):
    password = PasswordField()
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        write_only_fields = [
            'password',
        ]


class RegisterSerializer(serializers.Serializer):
    user = UserInfoSerializer()
    region = ProfileSerializer()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['pk'] = self.user.pk
        data['username'] = self.user.username
        data['region'] = self.user.profile.region
        return data


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
