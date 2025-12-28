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

# from django.shortcuts import render, redirect
# from .models import MoodRecord
# from django.db.models import Sum
# from django.views.decorators.http import require_POST
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.decorators import login_required  # 追加

# # ... (他のビューは変更なし)

# @login_required  # ログイン必須
# def feeling(request):
#     if request.method == 'POST':
#         mood = request.POST.get('mood')
#         amount = request.POST.get('amount')
#         if mood and amount:
#             try:
#                 amount_int = int(amount)
#                 MoodRecord.objects.create(user=request.user, mood=mood, amount=amount_int)
#                 return redirect('saving_list')  # 保存後に貯金リストページへリダイレクト
#             except ValueError:
#                 # 金額が無効な場合のエラーハンドリング（必要に応じて追加）
#                 pass
#     return render(request, "saving/feeling.html")