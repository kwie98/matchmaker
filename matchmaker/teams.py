from itertools import batched
from random import sample

type Team = tuple[str, ...]


def make_teams(team_size: int, players: list[str]) -> list[Team]:
    permutation = sample(players, k=len(players))
    return list(batched(permutation, team_size))
