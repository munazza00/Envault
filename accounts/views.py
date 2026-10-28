from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("project_dashboard")
    else:
        form = SignUpForm()

    return render(request, "accounts/auth.html", {
        "form": form,
        "title": "Create Account",
        "button_text": "Sign Up",
        "link_text": "Already have an account? Log in",
        "link_url": "user_login",
    })


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("project_dashboard")
    else:
        form = AuthenticationForm(request)

    return render(request, "accounts/auth.html", {
        "form": form,
        "title": "Welcome Back",
        "button_text": "Log In",
        "link_text": "Don't have an account? Sign up",
        "link_url": "signup",
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect("user_login")