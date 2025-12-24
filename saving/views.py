from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "saving/home.html")


def base(request):
    return render(request, "saving/base.html")


def roulette(request):
    return render(request, "saving/roulette.html")
