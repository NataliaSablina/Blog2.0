from django.urls import path
from post.views import CreatePostView, CategoryPostsView

urlpatterns = [
    path('create_post', CreatePostView.as_view(), name='create_post'),
    path('category_posts<int:pk>', CategoryPostsView.as_view(), name='category_posts')
]
