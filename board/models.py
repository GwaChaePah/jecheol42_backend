from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class Post(models.Model):
    TAGS = [
        (0, '소분'),
        (1, '나눔'),
        (2, '완료'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    image1 = models.ImageField(upload_to="posts/img/")
    image2 = models.ImageField(upload_to="posts/img/", blank=True, null=True)
    image3 = models.ImageField(upload_to="posts/img/", blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    # created_at = models.DateTimeField(default=timezone.now)
    # updated_at = AutoDateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.PositiveSmallIntegerField(choices=TAGS)
    price = models.PositiveIntegerField(default=0)
    user_key = models.PositiveIntegerField()


class Product(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="product/img")
    month = ArrayField(models.IntegerField(null=True), blank=True, size=12)


class Comment(models.Model):
    post_key = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=400, null=False)
    user_key = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OpenApi(models.Model):
    item_name = models.CharField(max_length=32)
    kind_name = models.CharField(max_length=32)
    rank = models.CharField(max_length=8)
    unit = models.CharField(max_length=8)
    date = models.CharField(max_length=16)
    price = models.CharField(max_length=8)
    average_price = models.CharField(max_length=8)
    created_at = models.DateTimeField(default=timezone.now)
