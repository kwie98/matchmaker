from django.urls import path

from . import views

app_name = "matchmaker"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("teams", views.TeamsView.as_view(), name="teams"),
    path("tournament", views.TournamentView.as_view(), name="tournament"),
]
