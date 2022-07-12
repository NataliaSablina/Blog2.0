from django.urls import path
from user.views import RegistrationView, UserAccountView, AuthenticationView

urlpatterns = [
    path('registration', RegistrationView.as_view(), name='registration'),
    path('authentication', AuthenticationView.as_view(), name='authentication'),
    path('user_account/<int:pk>', UserAccountView.as_view(), name='user_account')
]
