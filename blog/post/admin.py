from django.contrib import admin
from django.utils.safestring import mark_safe
from post.models import Post, Category
from django import forms


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class PostChangeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',  'photo', 'author', 'category')


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    add_form = PostChangeForm
    list_display = ('id', 'title', 'content',  'avatar_tag', 'author', 'creation_date', 'category')
    fields = ('content', 'title', 'author', 'category')

    readonly_fields = ['avatar_tag']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
