import random

from django.shortcuts import render
from datetime import datetime
from .models import Post, Comment, Product, OpenApi
from .open_api import put_data_to_api_table
from django.db.models import Q


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
    searchtext = '버섯'
    context = {
        # 'open_api_data': OpenApi.objects.all().order_by('id'),
        'open_api_data': OpenApi.objects.filter(Q(item_name__contains=searchtext) | Q(kind_name__contains=searchtext)).filter(rank='중품', date=date).order_by('id'),
    }
    return render(request, 'search.html', context)
