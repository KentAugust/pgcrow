"""Scenes config for game scenes"""

from typing import NamedTuple, Any, Protocol


class Scene2D(Protocol):

    def update(self, dt: float):
        """For updating stuff"""

    def render(self):
        """For rendering stuff"""


CallableScene = NamedTuple(
    "CallableScene", [("scene_class", "Scene2D"), ("kwargs", "dict[str, Any]")]
)
