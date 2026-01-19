from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDate, Coalesce
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import SavingRecord, Method
from .forms import CustomUserCreationForm, ProfileEditForm
from datetime import timedelta
import json
import random



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



@login_required
def rps(request):
    result = None
    cpu_hand = None
    diff = 0

    if request.method == "POST":
        user_hand = request.POST.get("hand")
        cpu_hand = random.choice(["グー", "チョキ", "パー"])

        BASE_AMOUNT = 100  # ← ジャンケン貯金の基本額

        if user_hand == cpu_hand:
            result = "あいこ"
            diff = 0

        elif (
            (user_hand == "グー" and cpu_hand == "チョキ") or
            (user_hand == "チョキ" and cpu_hand == "パー") or
            (user_hand == "パー" and cpu_hand == "グー")
        ):
            result = "勝ち"
            diff = BASE_AMOUNT

        else:
            result = "負け"
            diff = -BASE_AMOUNT

        if diff != 0:
            method, _ = Method.objects.get_or_create(
                method_name="ジャンケン貯金"
            )

            SavingRecord.objects.create(
                user=request.user,
                method=method,
                amount=diff,
                saved_at=timezone.localdate(),
            )

    return render(request, "saving/rps.html", {
        "result": result,
        "cpu_hand": cpu_hand,
        "diff": diff,
    })





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
    # 連続貯金日数の計算
    dates = (
        SavingRecord.objects.filter(user=request.user)
        .annotate(date=TruncDate("saved_at"))
        .values("date")
        .distinct()
        .order_by("date")
    )

    current_streak = 0
    if dates:
        dates_list = [d["date"] for d in dates]
        temp_streak = 1
        for i in range(1, len(dates_list)):
            if dates_list[i] - dates_list[i - 1] == timedelta(days=1):
                temp_streak += 1
            else:
                temp_streak = 1

        if dates_list[-1] == timezone.localdate():
            current_streak = temp_streak

    total_saving = get_total_saving(request.user)
    target_amount = request.user.target_amount
    achievement_rate = (
        int((total_saving / target_amount) * 100) if target_amount > 0 else 0
    )

    # 貯金履歴の取得（降順）
    saving_history = []
    history_dates = (
        SavingRecord.objects.filter(user=request.user)
        .annotate(date=TruncDate("saved_at"))
        .values("date")
        .distinct()
        .order_by("-date")
    )

    for date_obj in history_dates:
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
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "saving/profile-edit.html", {"form": form})
