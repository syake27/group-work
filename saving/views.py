from django.shortcuts import render, redirect
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


def roulette(request):
    return render(request, "saving/roulette.html")
def saving_list(request):
    return render(request, "saving/saving-list.html")


def ranking(request):
    return render(request, "saving/ranking.html")


def profile(request):
    return render(request, "saving/profile.html")
