from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from user.forms import RegistrationForm, AuthenticationForm
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
        context = {
            "user": user,
        }
        return render(request, "user_account.html", context)

