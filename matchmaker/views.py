from django import forms
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.urls import reverse

from matchmaker.teams import make_teams


class TeamsForm(forms.Form):
    team_size = forms.IntegerField(min_value=0, required=True, label="Teamgröße", initial=2)
    players = forms.CharField(required=True, label="Mitspieler", widget=forms.Textarea())


def index(request: HttpRequest) -> HttpResponse:
    """Display a form to input team size and players and handle form POST."""
    if request.method == "GET":
        return render(request, "matchmaker/index.html", {"form": TeamsForm()})

    form = TeamsForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()

    request.session["team_size"] = int(form.cleaned_data["team_size"])
    request.session["players"] = [
        player
        for line in form.cleaned_data["players"].splitlines()
        if (player := line.strip()) != ""
    ]
    return HttpResponseRedirect(reverse("matchmaker:teams"))


def teams(request: HttpRequest) -> HttpResponse:
    """Show generated teams and give the option of re-rolling or going back."""
    request.session["teams"] = make_teams(request.session["team_size"], request.session["players"])
    return render(request, "matchmaker/teams.html", {"teams": request.session["teams"]})
