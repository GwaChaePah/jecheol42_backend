from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }


class RegisterForm(UserCreationForm):
    local = forms.IntegerField()

    class Meta:
        model = User
        fields = (
            'username',
            'local',
        )

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'local': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }
