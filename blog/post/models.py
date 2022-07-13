from django.db import models
from django.utils.safestring import mark_safe

from user.models import User


class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name="Title")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    creation_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date of creation")
    title = models.CharField(max_length=250, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True, verbose_name="Photo")
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default="Without Category")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-creation_date"]

    def __str__(self):
        return self.title

    def get_avatar(self):
        if not self.photo:
            return '/static/images/user_icon.png'
        return self.photo.url

    def avatar_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())

    avatar_tag.short_description = 'Avatar'
