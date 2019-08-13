from django.forms import ModelForm, Textarea
from .models import Post


class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            'content': '',
        }