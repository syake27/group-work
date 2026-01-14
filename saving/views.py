from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from .models import SavingRecord, Method
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "saving/signup.html", {"form": form})


def home(request):
    total_saving = (
        SavingRecord.objects.filter(user=request.user).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )
    return render(
        request,
        "saving/home.html",
        {
            "total_saving": total_saving,
        },
    )


def base(request):
    return render(request, "saving/base.html")


def roulette(request):
    return render(request, "saving/roulette.html")


def saving_list(request):
    return render(request, "saving/saving-list.html")


def rps(request):
    return render(request, "saving/rps.html")


def ranking(request):
    return render(request, "saving/ranking.html")


def profile(request):
    return render(request, "saving/profile.html")


def simple(request):
    if request.method == "POST":
        amount = request.POST.get("amount")

        method = Method.objects.get(method_name="シンプル貯金")

        SavingRecord.objects.create(
            user=request.user,
            method=method,
            amount=amount,
            saved_at=timezone.now().date(),
        )

        return render(request, "saving/simple_done.html", {"amount": amount})

    return render(request, "saving/simple.html")


def feeling(request):
    if request.method == "POST":
        mood = request.POST.get("mood")

        if mood == "元気！！":
            amount = 500
        elif mood == "普通":
            amount = 200
        else:
            amount = 100

        method = Method.objects.get(method_name="気分貯金")

        SavingRecord.objects.create(
            user=request.user,
            method=method,
            amount=amount,
            saved_at=timezone.now().date(),
        )

        return render(request, "saving/simple_done.html", {"amount": amount})

    return render(request, "saving/feeling.html")
