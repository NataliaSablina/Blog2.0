from django.shortcuts import render, redirect
from django.views import View
from post.forms import CreatePostForm
from post.models import Category, Post


class CreatePostView(View):
    def get(self, request):
        post_form = CreatePostForm()
        context = {
            "post_form": post_form,
        }
        return render(request, "create_post.html", context)

    def post(self, request):
        post_form = CreatePostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.photo = request.FILES.get('photo')
            post.save()
            return redirect('home_page')
        else:
            print(post_form.errors)
            return redirect('create_post')


class CategoryPostsView(View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        categories = Category.objects.all()
        posts = Post.objects.filter(category=category)
        context = {
            "category": category,
            "posts": posts,
            "categories": categories,
        }
        return render(request, "category_posts.html", context)
