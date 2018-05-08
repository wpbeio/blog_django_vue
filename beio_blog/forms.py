from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """post的表单"""
    class Meta(object):
        """docstring for Meta"""
        model = Post
        fields = ('title', 'context','summary','tags','category')

        labels = {
            'title': ('标题'),
            'context': ('正文'),
            'summary':('摘要'),
            'category': ('分类'),
            'tags': ('标签'),
        }
