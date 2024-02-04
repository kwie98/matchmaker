import re
from itertools import batched
from random import sample
from typing import NamedTuple

TAILWIND_HUES = ["red", "orange", "yellow", "green", "cyan", "blue", "fuchsia", "pink"]


class Team(NamedTuple):
    hue: str
    members: tuple[str, ...]


def make_teams(team_size: int, player_groups: str) -> list[Team]:
    """Generate random teams.

    `player_groups` contains one or more groups of players, split by empty lines. The first group of
    players is assigned to random teams of size `team_size`. The remaining groups are each their own
    team.
    """
    # TODO overflow rest into bigger teams
    # Split on empty lines after trimming whitespace from start and end of user input:
    player_groups = re.sub(r"\r\n", r"\n", player_groups)
    groups: list[list[str]] = [
        group.splitlines() for group in re.split(r"[\n]{2,}", player_groups.strip())
    ]
    # Strip whitespace from each line (player name):
    groups_ = [tuple([player.strip() for player in group]) for group in groups]

    # Randomize first group:
    permutation = sample(groups_[0], k=len(groups_[0]))
    random_teams = list(batched(permutation, team_size))
    # Combine last two teams if the last team is too small:
    if len(random_teams) >= 2 and len(random_teams[-1]) < team_size:  # noqa: PLR2004
        random_teams.append(random_teams.pop() + random_teams.pop())
    teams = random_teams + groups_[1:]

    return [Team(hue, members) for (hue, members) in zip(TAILWIND_HUES, teams)]
