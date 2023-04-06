from django.forms import ModelForm, Select
from .models import Post


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['rating']

