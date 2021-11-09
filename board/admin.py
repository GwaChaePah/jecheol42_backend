from django.contrib import admin
from .models import Post, Comment, Product, OpenApi


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
        'price',
        'created_at',
        'updated_at',
        'user_key',
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
        'month',
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


@admin.register(OpenApi)
class OpenApiAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'item_name',
        'kind_name',
        'rank',
        'unit',
        'date',
        'price',
        'average_price',
        'created_at',
    )
    search_fields = (
        'item_name',
        'kind_name',
        'date',
    )
