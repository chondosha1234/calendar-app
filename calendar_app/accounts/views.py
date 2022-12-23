from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from accounts.forms import SignInForm, SignUpForm
# Create your views here.

class SignInView(View):
    template_name = "signin.html"
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("cal:calendar")
            else:
                print("didnt work")
        context = {
            "form": form
            #error
        }
        return render(request, self.template_name, context)


def signout(request):
    logout(request)
    return redirect("signin")


class SignUpView(View):
    template_name = "signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
