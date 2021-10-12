from django.contrib import admin
from .models import Post, Product, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'content',
        'image1',
        'image2',
        'image3',
        'view_count',
        'tag',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'title',
        'content',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'image',
        'jan',
        'feb',
        'mar',
        'apr',
        'may',
        'jun',
        'jul',
        'aug',
        'sep',
        'oct',
        'nov',
        'dec',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post_key',
        'content',
        'user_key',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'post_key',
        'user_key',
    )

