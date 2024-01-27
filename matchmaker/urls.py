from django.urls import path
from . import views


app_name = "matchmaker"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("teams", views.Teams.as_view(), name="teams"),
    path("tournament", views.Tournament.as_view(), name="tournament"),
    path("rounds/<int:round>", views.Round.as_view(), name="rounds"),
]
