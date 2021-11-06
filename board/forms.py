from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'tag',
            'content',
            'image1',
            'image2',
            'image3',
            'price',
            'user_key'
        ]
        labels = {
            'title': '제목',
            'content': '내용',
            'image1': '대표 사진',
            'price': '가격',
            'tag': '구분'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'user_key': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
            'user_key'
        ]
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'user_key': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            })
        }
