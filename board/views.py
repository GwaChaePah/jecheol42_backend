import random

from django.shortcuts import render
from datetime import datetime
from .models import Post, Comment, Product
from .open_api import call_open_api


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
    json_res = call_open_api()
    context = {
        'json': json_res
    }
    return render(request, 'search.html', context)
