from typing import Literal, NamedTuple

from matchmaker.teams import Team

PAUSE = Team("gray", ("Pause",))


type MatchState = Literal["LEFT_WON", "RIGHT_WON", "TBD"]


class Match(NamedTuple):
    left: Team
    right: Team
    state: MatchState


type Tournament = list[list[Match]]


def make_tournament(teams: list[Team]) -> Tournament:
    if len(teams) % 2 == 1:
        pivot = PAUSE
        circle = teams
    else:
        pivot = teams[0]
        circle = teams[1:]
    rounds: Tournament = []
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
        rounds.append(matches)
    return rounds


def count_wins(teams: list[Team], tournament: Tournament) -> dict[Team, int]:
    scores: dict[Team, int] = {team: 0 for team in teams}
    scores[PAUSE] = 0
    for rnd in tournament:
        for match in rnd:
            if match.state == "LEFT_WON":
                scores[match.left] += 1
            if match.state == "RIGHT_WON":
                scores[match.right] += 1
    del scores[PAUSE]
    return dict(sorted(scores.items(), key=lambda t: -t[1]))
