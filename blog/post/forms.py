from django import forms

from post.models import Post


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=250)
    content = forms.CharField(label="Content")
    photo = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('category', 'title', 'content', 'photo')