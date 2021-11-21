from datetime import datetime

from django.db.models import Q
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import generics, views, response, status, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Post, Comment, Product, OpenApi, Profile, Region

from . import serializers as ser


def set_permissions(self):
    try:
        origin = self.request.META['HTTP_REFERER']
    except:
        permission_classes = [permissions.IsAdminUser,]
    else:
        front = "https://jecheol42.herokuapp.com/"
        local = "http://127.0.0.1:8080/"
        if (origin == front) or (origin == local):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser, ]
    return [permission() for permission in permission_classes]


class ProductList(generics.ListAPIView):
    month = datetime.now().month
    queryset = Product.objects.filter(month__contains=[month]).order_by("?")[:4]
    serializer_class = ser.ProductSerializer

    def get_permissions(self):
        return set_permissions(self)


class BoardSearchList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = ser.BoardSerializer

    search_param = openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description='여기에 검색어를 넣고 execute 하세요',
        type=openapi.TYPE_STRING,
    )

    tag_param = openapi.Parameter(
        'tag',
        openapi.IN_QUERY,
        description='소분:0/나눔:1/완료:2 태그를 선택하세요',
        type=openapi.TYPE_INTEGER
    )

    region_param = openapi.Parameter(
        'region',
        openapi.IN_QUERY,
        description='지역 코드를 입력하세요',
        type=openapi.TYPE_INTEGER
    )

    def get_search(self, request):
        try:
            search_text = request.GET['search']
        except:
            return Post.objects.all().order_by('-id')
        return Post.objects.filter(Q(title__contains=search_text) | Q(content__contains=search_text)).order_by('-id')

    def get_tag(self, request, search_res):
        try:
            tag_type = request.GET['tag']
        except:
            return search_res.exclude(tag=2)
        return search_res.filter(tag=tag_type)

    def get_region(self, request, tag_res):
        try:
            region = request.GET['region']
        except:
            return tag_res
        city = int(region) / 100
        min = city * 100
        max = min + 100
        return tag_res.filter(user_key__profile__region__gte=min, user_key__profile__region__lt=max)

    def get_permissions(self):
        return set_permissions(self)

    @swagger_auto_schema(manual_parameters=[search_param, tag_param, region_param])
    def get(self, request, *args, **kwargs):
        search_res = self.get_search(request)
        tag_res = self.get_tag(request, search_res)
        result = self.get_region(request, tag_res)
        page = self.paginate_queryset(result)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ser.BoardSerializer(result, many=True)
        return response.Response(serializer.data)


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = ser.CommentSerializer

    def get_object(self, pk):
        try:
            return Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        comments = Comment.objects.filter(post_key=post).order_by('id')
        serializer = ser.CommentSerializer(comments, many=True)
        return response.Response(serializer.data)

    def get_permissions(self):
        return set_permissions(self)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = ser.PostSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)

    def get_permissions(self):
        return set_permissions(self)


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = ser.PostCreateSerializer
    parser_classes = (MultiPartParser,)

    def get_permissions(self):
        return set_permissions(self)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = ser.CommentCreateSerializer

    def get_permissions(self):
        return set_permissions(self)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = ser.CommentSerializer

    def get_permissions(self):
        return set_permissions(self)


class SearchList(views.APIView):
    search_param = openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description='여기에 검색어를 넣고 execute 하세요',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[search_param])
    def get(self, request):
        search_text = request.GET['search']
        queryset = OpenApi.objects.filter(item_name=search_text)
        if (not search_text.isalpha()) or ("g" in search_text):
            serializer = ser.SearchSerializer(queryset, many=True)
            return response.Response(serializer.data)
        if not len(queryset):
            queryset = OpenApi.objects.filter(kind_name__startswith=search_text)
        if not len(queryset):
            queryset = OpenApi.objects.filter(kind_name__contains=search_text)
        result = queryset.exclude(price="-").order_by('-id')
        serializer = ser.SearchSerializer(result, many=True)
        return response.Response(serializer.data)

    def get_permissions(self):
        return set_permissions(self)


class UserCheckView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ser.UserSerializer

    def post(self, request):
        request_name = request.data['username']
        try:
            user = User.objects.get(username=request_name)
        except:
            return response.Response(status=status.HTTP_202_ACCEPTED)
        return response.Response(status=status.HTTP_401_UNAUTHORIZED)

    def get_permissions(self):
        return set_permissions(self)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = ser.MyTokenObtainPairSerializer

    def get_permissions(self):
        return set_permissions(self)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ser.RegisterSerializer

    def set_profile(self, user_obj, region):
        profile = Profile.objects.create(user_key=user_obj)
        profile.region = region["region"]
        profile.save()

    def post(self, request, *args, **kwargs):
        user = request.data["user"]
        region = request.data["region"]
        user_serializer = ser.UserInfoSerializer(data=user)
        if user_serializer.is_valid():
            user_obj = User.objects.create(
                username=user["username"],
            )
            user_obj.set_password(user["password"])
            user_obj.save()
            self.set_profile(user_obj, region)
            return response.Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(user_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_permissions(self):
        return set_permissions(self)


class RegionList(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = ser.RegionSerializer

    def get_permissions(self):
        return set_permissions(self)

    region_param = openapi.Parameter(
        'search',
        openapi.IN_QUERY,
        description='여기에 해당 동을 입력하세요',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[region_param])
    def get(self, request, *args, **kwargs):
        try:
            search_address = request.GET['search']
        except:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        search_res = Region.objects.filter(address__contains=search_address)
        serializer = ser.RegionSerializer(search_res, many=True)
        return response.Response(serializer.data)
