from django.shortcuts import render
from django.views import View
from post.models import Post


class HomePageView(View):
    def get(self, request):
        posts = Post.objects.all()
        print(posts)
        context = {
            "posts": posts,
        }
        return render(request, "home_page.html", context)
