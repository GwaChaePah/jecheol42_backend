from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Post, Comment, Product, OpenApi
from django.db.models import Q
from .serializers import ProductSerializer, BoardSerializer, SearchSerializer
from rest_framework import generics, views, response
from django.http import Http404
from django.core import serializers
import json
from .forms import PostForm, CommentForm
from django.views.decorators.http import require_POST


def main(request):
    month = datetime.now().month
    context = {
        'products': Product.objects.filter(month__contains=[month]).order_by("?")[:4],
    }
    return render(request, 'main.html', context)


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
        'open_api_data': OpenApi.objects.filter(Q(item_name__contains=search_text) | Q(kind_name__contains=search_text)).filter(rank='중품', date=date).order_by('id'),
    }
    return render(request, 'search.html', context)


def new(request):
    context = {
        'form': PostForm()
    }
    return render(request, 'new.html', context)


@require_POST
def create(request):
    form = PostForm(request.POST, request.FILES or None)
    if form.is_valid():
        form.save()
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
    form = CommentForm(request.POST, request.FILES or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post_key = post
        comment.save()
    return redirect('show', post_key)


class ProductList(generics.ListAPIView):
    month = datetime.now().month
    queryset = Product.objects.filter(month__contains=[month]).order_by("?")[:4]
    serializer_class = ProductSerializer


class BoardList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = BoardSerializer


class PostList(views.APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        comments = Comment.objects.filter(post_key=post)
        post_list = [post]
        comments_list = list(comments)
        joined_list = post_list + comments_list
        json_str = serializers.serialize('json', joined_list)
        json_data = json.loads(json_str)
        return response.Response(json_data)


class SearchList(views.APIView):
    def get(self, request, search, format=None):
        search_res = OpenApi.objects.filter(Q(item_name__contains=search) | Q(kind_name__contains=search))
        serializer = SearchSerializer(search_res, many=True)
        return response.Response(serializer.data)
