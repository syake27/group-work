from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "saving/home.html")


def base(request):
    return render(request, "saving/base.html")


def saving_list(request):
    return render(request, "saving/saving-list.html")


def ranking(request):
    return render(request, "saving/ranking.html")


def profile(request):
    return render(request, "saving/profile.html")
