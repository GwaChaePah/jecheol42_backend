import random

from django.shortcuts import render
from datetime import datetime
from .models import Post, Comment, Product, OpenApi
from .open_api import put_data_to_api_table


def main(request):
    month = datetime.now().month
    context = {
        'products': Product.objects.filter(month__contains=[month]).order_by("?")[:2],
    }
    return render(request, 'main.html', context)


def board(request):
    context = {
        'posts': Post.objects.all().order_by('-created_at'),
        'comments': Comment.objects.all().order_by('created_at'),
    }
    return render(request, 'board.html', context)


def search(request):
    i = 1
    date = datetime.now().date()
    while i < 5:
        put_data_to_api_table(date, i * 100)
        i += 1
    context = {
        'open_api_data': OpenApi.objects.all().order_by('id'),
    }
    return render(request, 'search.html', context)
