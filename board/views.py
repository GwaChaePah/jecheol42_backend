from django.shortcuts import render
from datetime import datetime
from .models import Post, Comment, Product, OpenApi
from django.db.models import Q
from .serializers import ProductSerializer, BoardSerializer, CommentSerializer, SearchSerializer
from rest_framework import generics, views, response
from django.http import Http404


def main(request):
    month = datetime.now().month
    context = {
        'products': Product.objects.filter(month__contains=[month]).order_by("?")[:4],
    }
    return render(request, 'main.html', context)


def board(request):
    context = {
        'posts': Post.objects.all().order_by('-created_at'),
        'comments': Comment.objects.all().order_by('created_at'),
    }
    return render(request, 'board.html', context)


def search(request):
    date = datetime.now().date()
    search_text = '버섯'
    context = {
        # 'open_api_data': OpenApi.objects.all().order_by('id'),
        'open_api_data': OpenApi.objects.filter(Q(item_name__contains=search_text) | Q(kind_name__contains=search_text)).filter(rank='중품', date=date).order_by('id'),
    }
    return render(request, 'search.html', context)


class ProductList(generics.ListAPIView):
    month = datetime.now().month
    queryset = Product.objects.filter(month__contains=[month]).order_by("?")[:4]
    serializer_class = ProductSerializer


class BoardList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = BoardSerializer


class CommentList(views.APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        comments = Comment.objects.filter(post_key=post)
        serializer = CommentSerializer(comments, many=True)
        return response.Response(serializer.data)


class SearchList(views.APIView):
    def get(self, request, format=None):
        search_text = request.GET['search']
        search_res = OpenApi.objects.filter(Q(item_name__contains=search_text) | Q(kind_name__contains=search_text))
        serializer = SearchSerializer(search_res, many=True)
        return response.Response(serializer.data)
