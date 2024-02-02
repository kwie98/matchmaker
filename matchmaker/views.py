from django import forms
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from pydantic import BaseModel

from matchmaker.teams import Team, make_teams
from matchmaker.tournament import MatchState, Tournament, count_wins, make_tournament


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
                "placeholder": "Alejandro\nFernando\nRoberto\n...",
                "class": "min-w-full",
                "cols": 1,
            }
        ),
    )


class Session(BaseModel):
    team_size: int | None = None
    players: list[str] | None = None
    teams: list[Team] | None = None
    tournament: Tournament | None = None


class MatchUpdate(BaseModel):
    index: int
    new_state: MatchState


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Show a `TeamsForm` form for inputting team size and player names."""
        return render(request, "matchmaker/index.html", {"form": TeamsForm()})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Flush session, put inputs from `TeamsForm` form and redirect to the teams view."""
        form = TeamsForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()

        request.session.flush()
        request.session["team_size"] = int(form.cleaned_data["team_size"])
        request.session["players"] = [
            player
            for line in form.cleaned_data["players"].splitlines()
            if (player := line.strip()) != ""
        ]
        return HttpResponseRedirect(reverse("matchmaker:teams"))


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]
        self.status_code = 200


class TeamsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Generate teams and show them in a view."""
        session = Session(**request.session)
        if session.team_size is None or session.players is None:
            return HttpResponseBadRequest()

        teams = make_teams(session.team_size, session.players)
        request.session["teams"] = teams
        return render(request, "matchmaker/teams.html", {"teams": teams})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Generate tournament and redirect to the tournament view."""
        session = Session(**request.session)
        if session.teams is None:
            return HttpResponseBadRequest()

        request.session["tournament"] = make_tournament(session.teams)
        return HTTPResponseHXRedirect(reverse("matchmaker:tournament"))


class TournamentView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        """Show overview over the tournament (all rounds). TODO: Show scoreboard."""
        session = Session(**request.session)
        if session.teams is None or session.tournament is None:
            return HttpResponseBadRequest()

        scores = count_wins(session.teams, session.tournament)
        return render(
            request,
            "matchmaker/tournament.html",
            {"tournament": session.tournament, "scores": scores},
        )


class RoundView(View):
    def get(self, request: HttpRequest, rnd: int) -> HttpResponse:
        session = Session(**request.session)
        if session.tournament is None:
            return HttpResponseBadRequest()

        return render(
            request, "matchmaker/round.html", {"matches": session.tournament[rnd], "round": rnd}
        )

    def post(self, request: HttpRequest, rnd: int) -> HttpResponse:
        post = next(iter(request.POST.items()))
        match_update = MatchUpdate(index=post[0], new_state=post[1])

        request.session["tournament"][str(rnd)][match_update.index][2] = match_update.new_state
        request.session.modified = True
        return HttpResponse(status=204)
