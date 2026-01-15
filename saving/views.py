from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm, ProfileEditForm
from .models import SavingRecord, Method
from datetime import timedelta, date
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "saving/signup.html", {"form": form})


def get_total_saving(user):
    return (
        SavingRecord.objects.filter(user=user).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )


@login_required
def home(request):
    context = {
        "total_saving": get_total_saving(request.user),
    }
    return render(request, "saving/home.html", context)


def base(request):
    return render(request, "saving/base.html")


def roulette(request):
    return render(request, "saving/roulette.html")


def feeling(request):
    return render(request, "saving/feeling.html")


@login_required
def saving_list(request):
    return render(request, "saving/saving-list.html")


def rps(request):
    return render(request, "saving/rps.html")


@login_required
def ranking(request):
    User = get_user_model()
    users = (
        User.objects.annotate(total=Coalesce(Sum("savingrecord__amount"), 0))
        .order_by("-total", "username", "id")
        .only("id", "username", "user_icon")
    )

    ranking_list = []
    for idx, user in enumerate(users, start=1):
        ranking_list.append(
            {
                "rank": idx,
                "username": user.username,
                "total": user.total,
                "total_display": f"¥{user.total:,}",
                "user_icon": user.user_icon.url if user.user_icon else "",
                "is_current": user.id == request.user.id,
            }
        )

    context = {
        "top1": ranking_list[0] if len(ranking_list) >= 1 else None,
        "top2": ranking_list[1] if len(ranking_list) >= 2 else None,
        "top3": ranking_list[2] if len(ranking_list) >= 3 else None,
        "rest": ranking_list[3:],
    }
    return render(request, "saving/ranking.html", context)


@login_required
def profile(request):
    total_saving = get_total_saving(request.user)

    dates = (
        SavingRecord.objects.filter(user=request.user)
        .values_list("saved_at", flat=True)
        .order_by("saved_at")
        .distinct()
    )

    current_streak = 0
    total_days = 0
    max_streak = 0

    if dates:
        dates = list(dates)
        total_days = len(dates)

        temp_streak = 1
        max_streak = 1

        for i in range(1, len(dates)):
            if dates[i] - dates[i - 1] == timedelta(days=1):
                temp_streak += 1
            else:
                max_streak = max(max_streak, temp_streak)
                temp_streak = 1

        max_streak = max(max_streak, temp_streak)

        today = date.today()
        if today - dates[-1] == timedelta(days=0):
            current_streak = temp_streak
        else:
            current_streak = 0

    context = {
        "user_name": request.user.username,
        "total_saving": total_saving,
        "current_streak": current_streak,
        "total_days": total_days,
        "max_streak": max_streak,
    }
    return render(request, "saving/profile.html", context)


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


def dice(request):
    return render(request, "saving/dice.html")


def edit_target(request):
    return render(request, "saving/edit_target.html")


def edit_profile(request):
    return render(request, "saving/edit_profile.html")


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "saving/profile-edit.html", {"form": form})
