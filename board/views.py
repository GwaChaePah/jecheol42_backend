from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Post, Comment, Product, OpenApi
from django.db.models import Q
from .serializers import ProductSerializer, BoardSerializer, PostDetailSerializer, PostSerializer, SearchSerializer
from rest_framework import generics, views, response, permissions, status
from django.http import Http404
from django.core import serializers
from .forms import PostForm, CommentForm, LoginForm
from django.views.decorators.http import require_POST
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from collections import namedtuple


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
    serializer_class = ProductSerializer


class BoardList(views.APIView):
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
            return search_res
        return search_res.filter(tag=tag_type)

    @swagger_auto_schema(manual_parameters=[search_param, tag_param])
    def get(self, request):
        search_res = self.get_search(request)
        result = self.get_tag(request, search_res)
        serializer = BoardSerializer(result, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostList(views.APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        comments = Comment.objects.filter(post_key=post).order_by('id')
        Detail = namedtuple('Detail', ('post', 'comments'))
        detail = Detail(
            post=post,
            comments=comments,
        )
        serializer = PostDetailSerializer(detail)
        return response.Response(serializer.data)

    # post_param = openapi.Parameter(
    #     'title',
    #     openapi.IN_QUERY,
    #     description='여기에 검색어를 넣고 execute 하세요',
    #     type=openapi.TYPE_STRING,
    # )
    #
    # @swagger_auto_schema(manual_parameters=[post_param])
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


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
        search_res = OpenApi.objects.filter(Q(item_name=search_text) | Q(kind_name__startswith=search_text))
        result = search_res.exclude(price="-").order_by('-id')
        serializer = SearchSerializer(result, many=True)
        return response.Response(serializer.data)


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


class TestView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        content = {'message': 'gwachaepah'}
        return response.Response(content)
