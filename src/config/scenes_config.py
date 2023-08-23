"""Scenes config for game scenes"""

from typing import NamedTuple, Any
from abc import ABC


Game = NamedTuple("Game", [("window", "Any")])


class Scene2D(ABC):
    """Abstract Class representing a single game scene"""

    def __init__(self, game: Game) -> None:
        ...

    def update(self, dt: float):
        """For updating stuff"""

    def render(self):
        """For rendering stuff"""


CallableScene = NamedTuple(
    "CallableScene", [("scene_class", "Scene2D"), ("kwargs", "dict[str, Any]")]
)
