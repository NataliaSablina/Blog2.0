from django.shortcuts import render
from django.views import View
from post.models import Post, Category


class HomePageView(View):
    def get(self, request):
        posts = Post.objects.all()
        categories = Category.objects.all()
        print(posts)
        context = {
            "posts": posts,
            "categories": categories,
        }
        return render(request, "home_page.html", context)
