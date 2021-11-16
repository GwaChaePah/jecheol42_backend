from random import choice
from datetime import datetime

from django.db.models import Q
from django.http import Http404
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import generics, views, response, status
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Post, Comment, Product, OpenApi
from .forms import PostForm, CommentForm, LoginForm, RegisterForm

from . import serializers as ser


def main(request):
    month = datetime.now().month
    context = {
        'products': Product.objects.filter(month__contains=[month]).order_by("?")[:4],
        'form': LoginForm()
    }
    return render(request, 'main.html', context)


@login_required
def board(request):
    context = {
        'posts': Post.objects.all().order_by('-created_at'),
    }
    return render(request, 'board.html', context)


def show(request, post_key):
    post = get_object_or_404(Post, pk=post_key)
    post.view_count += 1
    post.save()
    context = {
        'post': post,
        'comments': Comment.objects.filter(post_key=post).order_by('created_at'),
        'comment_form': CommentForm()
    }
    return render(request, 'show.html', context)


def search(request):
    date = datetime.now().date()
    search_text = '버섯'
    context = {
        # 'open_api_data': OpenApi.objects.all().order_by('id'),
        'open_api_data': OpenApi.objects.filter(
            Q(item_name__contains=search_text) | Q(kind_name__contains=search_text)).filter(rank='중품',
                                                                                            date=date).order_by('id'),
    }
    return render(request, 'search.html', context)


@login_required
def new(request):
    context = {
        'form': PostForm()
    }
    return render(request, 'new.html', context)


@require_POST
def create(request):
    form = PostForm(request.POST, request.FILES or None)
    user = request.user
    if form.is_valid():
        post = form.save(commit=False)
        post.user_key = user
        post.save()
    return redirect('board')


def edit(request, post_key):
    post = get_object_or_404(Post, pk=post_key)
    context = {
        'form': PostForm(instance=post),
        'post': post
    }
    return render(request, 'edit.html', context)


@require_POST
def update(request, post_key):
    post = get_object_or_404(Post, pk=post_key)
    form = PostForm(request.POST, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
    return redirect('show', post_key)


@require_POST
def delete(request, post_key):
    post = get_object_or_404(Post, pk=post_key)
    post.delete()
    return redirect('board')


@require_POST
def comment_create(request, post_key):
    post = get_object_or_404(Post, pk=post_key)
    user = request.user
    form = CommentForm(request.POST, request.FILES or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post_key = post
        comment.user_key = user
        comment.save()
    return redirect('show', post_key)


@require_POST
def comment_update(request, comment_key):
    comment = get_object_or_404(Comment, pk=comment_key)
    form = CommentForm(request.POST, request.FILES or None, instance=comment)
    if form.is_valid():
        form.save()
    return redirect('show', comment.post_key.pk)


@require_POST
def comment_delete(request, comment_key):
    comment = get_object_or_404(Comment, pk=comment_key)
    comment.delete()
    return redirect('show', comment.post_key.pk)


class ProductList(generics.ListAPIView):
    month = datetime.now().month
    queryset = Product.objects.filter(month__contains=[month]).order_by("?")[:4]
    serializer_class = ser.ProductSerializer


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

    @swagger_auto_schema(manual_parameters=[search_param, tag_param])
    def get(self, request, *args, **kwargs):
        search_res = self.get_search(request)
        result = self.get_tag(request, search_res)
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


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = ser.PostCreateSerializer
    parser_classes = (MultiPartParser,)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = ser.CommentCreateSerializer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = ser.CommentSerializer


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
        queryset.exclude(price="-").order_by('-id')
        serializer = ser.SearchSerializer(queryset, many=True)
        return response.Response(serializer.data)


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


def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('board')
    else:
        return redirect('main')


def user_logout(request):
    logout(request)
    return redirect('main')


def register(request):
    context = {
        'form': RegisterForm()
    }
    return render(request, 'user_register.html', context)


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.region = form.cleaned_data.get('region')
            user.save()
            return redirect('main')
    else:
        form = RegisterForm()
    return render(request, 'user_register.html', {'form': form})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = ser.MyTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ser.RegisterSerializer

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
            user_obj.refresh_from_db()
            user_obj.profile.region = region["region"]
            user_obj.save()
            return response.Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(user_serializer.errors, status=status.HTTP_418_IM_A_TEAPOT)
