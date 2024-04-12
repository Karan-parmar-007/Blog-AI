# forms.py
from django import forms
from .models import Post, Comment, Category, AnonymousPost

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'cat', 'post_image', 'video_file']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]



class SummaryForm(forms.Form):
    summary = forms.CharField(label='Summary', widget=forms.Textarea)

class AnonymousPostForm(forms.ModelForm):
    captcha = forms.CharField(label='Enter the CAPTCHA')
    class Meta:
        model = AnonymousPost
        fields = ['title', 'image', 'video', 'content']