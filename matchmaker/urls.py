from django.urls import path
from . import views


app_name = "matchmaker"
urlpatterns = [
    path("", views.index, name="index"),
    path("teams", views.teams, name="teams"),
    path("tournament", views.tournament, name="tournament")
]
