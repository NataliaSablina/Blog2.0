from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View
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
        reg_from = RegistrationForm(request.POST)
        if reg_from.is_valid():
            user = reg_from.save(commit=False)
            user.set_password(reg_from.cleaned_data["password2"])
            user.save()
            login(request, user)
            return redirect('user_account', user.pk)
        else:
            print(reg_from.errors)


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
            print(auth_form.errors)


class UserAccountView(View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        context = {
            "user": user,
        }
        return render(request, "user_account.html", context)

