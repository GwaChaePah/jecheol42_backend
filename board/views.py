from django.shortcuts import render
from .models import Post, Product, Comment


def main(request):
    context = {
        'product': Product.objects.all()
    }
    return render(request, 'main.html', context)


def board(request):
    context = {
        'posts': Post.objects.all().order_by('-created_at'),
        'comments': Comment.objects.all().order_by('-created_at'),
    }
    return render(request, 'board.html', context)

