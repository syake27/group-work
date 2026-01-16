from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required
from .models import SavingRecord, Method
from .forms import CustomUserCreationForm
from datetime import timedelta
import json


# --------------------
# 認証・基本ページ
# --------------------


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "saving/signup.html", {"form": form})


def base(request):
    return render(request, "saving/base.html")


def dice(request):
    return render(request, "saving/dice.html")


def roulette(request):
    return render(request, "saving/roulette.html")


def saving_list(request):
    return render(request, "saving/saving-list.html")


def rps(request):
    return render(request, "saving/rps.html")


def ranking(request):
    return render(request, "saving/ranking.html")


# --------------------
# 集計用ユーティリティ
# --------------------


def get_today_saving(user):
    today = timezone.localdate()
    return (
        SavingRecord.objects.filter(user=user, saved_at=today).aggregate(Sum("amount"))[
            "amount__sum"
        ]
        or 0
    )


def get_month_saving(user):
    today = timezone.localdate()
    start_of_month = today.replace(day=1)
    return (
        SavingRecord.objects.filter(user=user, saved_at__gte=start_of_month).aggregate(
            Sum("amount")
        )["amount__sum"]
        or 0
    )


def get_total_saving(user):
    return (
        SavingRecord.objects.filter(user=user).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )


# --------------------
# ホーム
# --------------------


@login_required
def home(request):
    dates = (
        SavingRecord.objects.filter(user=request.user)
        .values_list("saved_at", flat=True)
        .order_by("saved_at")
        .distinct()
    )

    current_streak = 0
    if dates:
        dates = list(dates)
        temp_streak = 1
        for i in range(1, len(dates)):
            if dates[i] - dates[i - 1] == timedelta(days=1):
                temp_streak += 1
            else:
                temp_streak = 1

        if dates[-1] == timezone.localdate():
            current_streak = temp_streak

    total_saving = get_total_saving(request.user)
    target_amount = request.user.target_amount
    achievement_rate = (
        int((total_saving / target_amount) * 100) if target_amount > 0 else 0
    )

    saving_history = []
    dates = (
        SavingRecord.objects.filter(user=request.user)
        .annotate(date=TruncDate("saved_at"))
        .values("date")
        .distinct()
        .order_by("-date")
    )

    for date_obj in dates:
        saved_date = date_obj["date"]
        total = SavingRecord.objects.filter(
            user=request.user, saved_at=saved_date
        ).aggregate(Sum("amount"))["amount__sum"]

        records = (
            SavingRecord.objects.filter(user=request.user, saved_at=saved_date)
            .select_related("method")
            .order_by("-created_at")
        )

        saving_history.append({"date": saved_date, "total": total, "records": records})

    graph_labels = [d["date"].strftime("%m/%d") for d in saving_history]
    graph_data = [d["total"] for d in saving_history]
    graph_data_json = json.dumps({"labels": graph_labels, "data": graph_data})

    context = {
        "total_saving": total_saving,
        "today_saving": get_today_saving(request.user),
        "month_saving": get_month_saving(request.user),
        "current_streak": current_streak,
        "achievement_rate": achievement_rate,
        "target_amount": target_amount,
        "saving_history": saving_history,
        "graph_data": graph_data_json,
    }
    return render(request, "saving/home.html", context)


# --------------------
# プロフィール
# --------------------


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

        if dates[-1] == timezone.localdate():
            current_streak = temp_streak

    context = {
        "user_name": request.user.username,
        "total_saving": total_saving,
        "current_streak": current_streak,
        "total_days": total_days,
        "max_streak": max_streak,
        "target_amount": request.user.target_amount,
    }
    return render(request, "saving/profile.html", context)


# --------------------
# 貯金処理
# --------------------


@login_required
def simple(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        method = Method.objects.get(method_name="シンプル貯金")

        SavingRecord.objects.create(
            user=request.user,
            method=method,
            amount=amount,
            saved_at=timezone.localdate(),
        )

        return render(request, "saving/simple_done.html", {"amount": amount})

    return render(request, "saving/simple.html")


@login_required
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
            saved_at=timezone.localdate(),
        )

        return render(request, "saving/simple_done.html", {"amount": amount})

    return render(request, "saving/feeling.html")


# --------------------
# 設定系
# --------------------


@login_required
def edit_target(request):
    if request.method == "POST":
        target_amount = request.POST.get("target_amount")
        if target_amount:
            request.user.target_amount = int(target_amount)
            request.user.save()
            return redirect("profile")
    return render(request, "saving/edit_target.html")


@login_required
def profile_edit(request):
    return render(request, "saving/profile-edit.html")
