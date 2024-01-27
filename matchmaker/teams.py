from itertools import batched
from random import sample
from typing import NamedTuple

TAILWIND_HUES = ["red", "orange", "yellow", "green", "cyan", "blue", "fuchsia", "pink"]


class Team(NamedTuple):
    hue: str
    members: list[str]

def make_teams(team_size: int, players: list[str]) -> list[Team]:
    permutation = sample(players, k=len(players))
    return list(
        Team(hue, list(members))
        for (hue, members) in zip(TAILWIND_HUES, batched(permutation, team_size))
    )
