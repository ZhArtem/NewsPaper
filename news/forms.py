from django import forms
from django.forms import ModelForm, Select
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

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


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='common')[0]
        basic_group.user_set.add(user)
        return user
