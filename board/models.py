from django.db import models


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


class Product(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="product/img")
    jan = models.BooleanField(default=False)
    feb = models.BooleanField(default=False)
    mar = models.BooleanField(default=False)
    apr = models.BooleanField(default=False)
    may = models.BooleanField(default=False)
    jun = models.BooleanField(default=False)
    jul = models.BooleanField(default=False)
    aug = models.BooleanField(default=False)
    sep = models.BooleanField(default=False)
    oct = models.BooleanField(default=False)
    nov = models.BooleanField(default=False)
    dec = models.BooleanField(default=False)
