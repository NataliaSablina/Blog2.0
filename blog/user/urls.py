from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from user.views import RegistrationView, UserAccountView, AuthenticationView, HelpUserView, ResetPasswordView

urlpatterns = [
    path('registration', RegistrationView.as_view(), name='registration'),
    path('authentication', AuthenticationView.as_view(), name='authentication'),
    path('user_account/<int:pk>', UserAccountView.as_view(), name='user_account'),
    path('help', HelpUserView.as_view(), name='help'),
    path('password_reset', ResetPasswordView.as_view(), name="password_reset"),
    path('password_reset_confirm/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/complete',
         PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
