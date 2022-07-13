from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse, BadHeaderError
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.contrib import messages

from blog import settings
from post.models import Post
from user.forms import RegistrationForm, AuthenticationForm, HelpUserForm, ContactForm
from user.models import User


class RegistrationView(View):
    def get(self, request):
        reg_form = RegistrationForm()
        context = {
            "reg_form": reg_form,
        }
        return render(request, "registration_form.html", context)

    def post(self, request):
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            user.set_password(reg_form.cleaned_data["password2"])
            user.save()
            login(request, user)
            return redirect('user_account', user.pk)
        else:
            for field, errors in reg_form.errors.items():
                messages.error(request, errors)
            return redirect('registration')


class AuthenticationView(View):
    def get(self, request):
        auth_form = AuthenticationForm()
        context = {
            "auth_form": auth_form,
        }
        return render(request, "authentication_form.html", context)

    def post(self, request):
        auth_form = AuthenticationForm(request.POST)
        if auth_form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('user_account', user.pk)
            else:
                messages.error(request, "You entered wrong email or password")
                return redirect('authentication')
        else:
            for field, errors in auth_form.errors.items():
                messages.error(request, errors)
            return redirect('authentication')


class UserAccountView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        posts = Post.objects.filter(author=user)
        context = {
            "user": user,
            "posts": posts,
        }
        return render(request, "user_account.html", context)


class HelpUserView(LoginRequiredMixin, View):
    login_url = 'home_page'

    def get(self, request):
        help_user_form = HelpUserForm()
        context = {
            "help_user_form": help_user_form,
        }
        return render(request, "help_user_form.html", context)

    def post(self, request):
        help_user_form = HelpUserForm(request.POST)
        if help_user_form.is_valid():
            subject = "Help for client"
            from_email = help_user_form.cleaned_data["email"]
            message = help_user_form.cleaned_data["message"]
            if from_email == request.user.email:
                try:
                    send_mail(subject, message, from_email, [settings.EMAIL_HOST_USER], fail_silently=False)
                    messages.error(request, 'Mail is sent successful')
                except BadHeaderError:
                    messages.error(request, 'Send email wrong')
                    return redirect('help')
                return redirect('home_page')
            else:
                messages.error(request, 'Your email is wrong')
        return redirect('help')


class ResetPasswordView(View):
    def get(self, request):
        form = ContactForm()
        context = {
            "form": form,
        }
        return render(request, "reset_password.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Reset password link"
            message = "Reset password link:"
            to_email = form.cleaned_data['to_email']
            email_template_name = "message_html.html"
            user = User.objects.get(email=to_email)
            cont = {
                "email": user.email,
                'domain': '127.0.0.1:8000',  # доменное имя сайта
                'site_name': 'Blog',  # название своего сайта
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),  # шифруем идентификатор
                "user": to_email,  # чтобы обратиться в письме по логину пользователя
                'token': default_token_generator.make_token(user),  # генерируем токен
                'protocol': 'http',
            }
            ref = cont.get('protocol') + '://' + cont.get('domain') + '/user/' + 'password_reset_confirm/' + str(
                cont.get('uid')) + '/' + str(cont.get('token'))
            msg_html = render_to_string(email_template_name, {"ref": ref})
            try:
                # send_mail(subject, message=ref, from_email=settings.EMAIL_HOST_USER, recipient_list=[to_email],
                #           fail_silently=False)
                send_mail(subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[to_email],
                          fail_silently=False, html_message=msg_html)
                # send_mail(subject, message, from_email, [settings.EMAIL_HOST_USER], fail_silently=False)
                messages.error(request, 'Mail is sent successful')
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('home_page')
        else:
            messages.error(request, "Wrong")
            return redirect('password_reset')
