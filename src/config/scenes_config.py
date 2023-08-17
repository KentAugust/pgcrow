"""Scenes config for game scenes"""

from typing import NamedTuple, Any

Scene2D = NamedTuple("Scene2D", [("game", "Any")])

CallableScene = NamedTuple(
    "CallableScene", [("scene_class", "Scene2D"), ("kwargs", "dict[str, Any]")]
)
