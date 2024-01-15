from django import forms
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matchmaker.teams import make_teams
from matchmaker.tournament import make_tournament


class TeamsForm(forms.Form):
    team_size = forms.IntegerField(
        label="Teamgröße",
        min_value=1,
        required=True,
        widget=forms.NumberInput(
            attrs={
                "value": "2",
                "class": "min-w-full",
                "size": 1,
            }
        ),
    )
    players = forms.CharField(
        label="Mitspieler",
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Fernando\nLewis\n...",
                "class": "min-w-full",
                "cols": 1,
            }
        ),
    )


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


def tournament(request: HttpRequest) -> HttpResponse:
    """Show overview over the tournament (all rounds). TODO: Show scoreboard."""
    request.session["tournament"] = make_tournament(request.session["teams"])
    return render(
        request, "matchmaker/tournament.html", {"tournament": request.session["tournament"]}
    )


def round(request: HttpRequest, round: int) -> HttpResponse:
    """TODO: Show details of a round, giving the option to post a match's result."""
    return HttpResponse(f"{request.session['tournament'][round - 1]}")
