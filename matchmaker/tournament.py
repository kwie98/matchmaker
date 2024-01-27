from typing import Literal, NamedTuple
from matchmaker.teams import Team


type MatchState = Literal["LEFT_WON"] | Literal["RIGHT_WON"] | Literal["TBD"]


class Match(NamedTuple):
    left: Team
    right: Team
    state: MatchState


type Tournament = dict[int, list[Match]]


def make_tournament(teams: list[Team]) -> Tournament:
    if len(teams) % 2 == 1:
        pivot = Team("gray", ("Pause",))
        circle = teams
    else:
        pivot = teams[0]
        circle = teams[1:]
    rounds: Tournament = {}
    for pivot_i in range(len(circle)):  # Rounds
        # The pivot team plays each other team in order:
        matches = [Match(pivot, circle[pivot_i], "TBD")]
        # The other match-ups are (pivot_i - 1, pivot_i + 1), (pivot_i - 2, pivot_i + 2), etc.
        for offset in range(1, len(circle) // 2 + 1):
            matches.append(
                Match(
                    circle[(pivot_i - offset) % len(circle)],
                    circle[(pivot_i + offset) % len(circle)],
                    "TBD",
                )
            )
        rounds[pivot_i + 1] = matches
    return rounds


def count_wins(tournament: Tournament) -> dict[Team, int]:
    pass # TODO
