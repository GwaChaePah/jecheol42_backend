from django.contrib import admin
from .models import Post


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
