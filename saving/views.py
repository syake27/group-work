from django.shortcuts import render, redirect
from .models import MoodRecord
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "saving/signup.html", {"form": form})


def home(request):
    return render(request, "saving/home.html")


def base(request):
    return render(request, "saving/base.html")


def feeling(request):
    return render(request, "saving/feeling.html")


def saving_list(request):
    return render(request, "saving/saving-list.html")


def rps(request):
    return render(request, "saving/rps.html")


def ranking(request):
    return render(request, "saving/ranking.html")


def profile(request):
    return render(request, "saving/profile.html")
