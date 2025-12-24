from django.shortcuts import render, redirect
from .models import MoodRecord
from django.db.models import Sum
from django.views.decorators.http import require_POST

# Create your views here.


def home(request):
    return render(request, "saving/home.html")


def base(request):
    return render(request, "saving/base.html")


def feeling(request):
    return render(request, "saving/feeling.html")


def saving_list(request):
    return render(request, "saving/saving-list.html")
