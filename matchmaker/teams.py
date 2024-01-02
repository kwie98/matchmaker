from itertools import batched
from random import sample

type Teams = list[tuple[str, ...]]


def make_teams(team_size: int, players: list[str]) -> Teams:
    permutation = sample(players, k=len(players))
    return list(batched(permutation, team_size))
