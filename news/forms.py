from django import forms
from django.forms import ModelForm, Select
from .models import Post


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['rating']
        widgets = {
            'author': forms.Select(attrs={
                'class': 'form-control'
            }),
            'categoryType': forms.Select(attrs={
                'class': 'form-control'
            }),
            'postCategory': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control'
            }),
        }
