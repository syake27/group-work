from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("base/", views.base, name="base"),
    path("saving-list/", views.saving_list, name="saving_list"),
    path("ranking/", views.ranking, name="ranking"),
    path("profile/", views.profile, name="profile"),
]
