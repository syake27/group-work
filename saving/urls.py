from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("base/", views.base, name="base"),
    path("roulette/", views.roulette, name="roulette"),
    path("feeling/", views.feeling, name="feeling"),
    path("saving-list/", views.saving_list, name="saving_list"),
    path("rps/", views.rps, name="rps"),
    path("ranking/", views.ranking, name="ranking"),
    path("profile/", views.profile, name="profile"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="saving/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("simple/", views.simple, name="simple"),
    path("dice/", views.dice, name="dice"),
    path("edit-target/", views.edit_target, name="edit_target"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("profile-edit/", views.profile_edit, name="profile_edit"),
]
