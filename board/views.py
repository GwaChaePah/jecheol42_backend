from django.shortcuts import render
from datetime import datetime
from .models import Post, Comment, ProductMonth


def main(request):
    month = datetime.now().month
    context = {
        'products': ProductMonth.objects.filter(month__contains=[month])
    }
    return render(request, 'main.html', context)


def board(request):
    context = {
        'posts': Post.objects.all().order_by('-created_at'),
        'comments': Comment.objects.all().order_by('created_at'),
    }
    return render(request, 'board.html', context)

