from django.urls import path
from home_page.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view()),
    path('home_page', HomePageView.as_view(), name='home_page')
]
