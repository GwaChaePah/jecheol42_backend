from django.shortcuts import render
from datetime import datetime
from .models import Post, Product, Comment, ProductMonth


def main(request):
    month = datetime.now().month
    if month == 10:
        context = {
            'product': Product.objects.filter(oct=1)
        }
    return render(request, 'main.html', context)


def board(request):
    context = {
        'posts': Post.objects.all().order_by('-created_at'),
        'comments': Comment.objects.all().order_by('created_at'),
    }
    return render(request, 'board.html', context)

