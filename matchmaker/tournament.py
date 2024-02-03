from typing import Literal, Self

from django.http.request import QueryDict
from pydantic import BaseModel

from matchmaker.teams import Team

PAUSE = Team("gray", ("Pause",))
type MatchResult = Literal["LEFT_WON", "RIGHT_WON", "TBD"]
type RoundState = Literal["DONE", "CURRENT", "FUTURE"]


class Match(BaseModel):
    left: Team
    right: Team
    result: MatchResult


class Round(BaseModel):
    matches: list[Match]
    state: RoundState

    def get_state_hue(self) -> str:
        match self.state:
            case "DONE":
                return "green"
            case "CURRENT":
                return "blue"
            case "FUTURE":
                return "gray"


class MatchUpdate(BaseModel):
    round: int
    match: int
    result: MatchResult

    @classmethod
    def from_post(cls, post: QueryDict) -> Self:
        rnd = post["round"]
        match = post["match"]
        result = post[f"result_{rnd}_{match}"]
        return cls(round=rnd, match=match, result=result)  # pyright: ignore [reportArgumentType]


class Tournament(BaseModel):
    rounds: list[Round]

    def set_match_result(self, update: MatchUpdate) -> None:
        self.rounds[update.round].matches[update.match].result = update.result

        # Update round states:
        found_current = False
        for r in self.rounds:
            if found_current:
                r.state = "FUTURE"
                continue
            if len([m.result for m in r.matches if m.result == "TBD"]) > 0:
                r.state = "CURRENT"
                found_current = True
                continue
            r.state = "DONE"

    @classmethod
    def from_rounds(cls, rounds: list[list[Match]]) -> Self:
        tournament = cls(rounds=[Round(matches=matches, state="FUTURE") for matches in rounds])
        tournament.rounds[0].state = "CURRENT"
        return tournament


def make_tournament(teams: list[Team]) -> Tournament:
    if len(teams) % 2 == 1:
        pivot = PAUSE
        circle = teams
    else:
        pivot = teams[0]
        circle = teams[1:]
    rounds: list[list[Match]] = []
    for pivot_i in range(len(circle)):  # Rounds
        # The pivot team plays each other team in order:
        matches = [Match(left=pivot, right=circle[pivot_i], result="TBD")]
        # The other match-ups are (pivot_i - 1, pivot_i + 1), (pivot_i - 2, pivot_i + 2), etc.
        for offset in range(1, len(circle) // 2 + 1):
            matches.append(
                Match(
                    left=circle[(pivot_i - offset) % len(circle)],
                    right=circle[(pivot_i + offset) % len(circle)],
                    result="TBD",
                )
            )
        rounds.append(matches)
    return Tournament.from_rounds(rounds)


def count_wins(teams: list[Team], tournament: Tournament) -> dict[Team, int]:
    scores: dict[Team, int] = {team: 0 for team in teams}
    scores[PAUSE] = 0
    for rnd in tournament.rounds:
        for match in rnd.matches:
            if match.result == "LEFT_WON":
                scores[match.left] += 1
            if match.result == "RIGHT_WON":
                scores[match.right] += 1
    del scores[PAUSE]
    return dict(sorted(scores.items(), key=lambda t: -t[1]))
