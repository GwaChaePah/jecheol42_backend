from django.shortcuts import render
from .models import Post


def main(request):
    return render(request, 'main.html')


def board(request):
    context = {
        'posts': Post.objects.all().order_by('-created_at')
    }
    return render(request, 'board.html', context)
