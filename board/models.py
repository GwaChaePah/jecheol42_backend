from django.db import models
from django.contrib.postgres.fields import ArrayField


class Post(models.Model):
    TAGS = [
        (0, '소분'),
        (1, '나눔'),
        (2, '완료'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    image1 = models.ImageField(upload_to="posts/img")
    image2 = models.ImageField(upload_to="posts/img", blank=True, null=True)
    image3 = models.ImageField(upload_to="posts/img", blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    tag = models.PositiveSmallIntegerField(choices=TAGS)
    price = models.PositiveIntegerField(default=0, blank=True, null=True)
    user_key = models.PositiveIntegerField()


class ProductMonth(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="product/img")
    month = ArrayField(models.IntegerField(null=True), blank=True, size=12)


class Comment(models.Model):
    post_key = models.PositiveIntegerField(null=False)
    content = models.TextField(max_length=400, null=False)
    user_key = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
