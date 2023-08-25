"""Config
module for setting different type of configuration needed for other classes"""

import pygame

from dataclasses import dataclass
from typing import NamedTuple, Any, Protocol
from abc import ABC


@dataclass
class WindowConfig:
    """Window configuration class"""

    window_size: tuple[int, int]
    display_size: tuple[int, int] | None = None
    scale_factor: float = 1.0
    avalible_window_sizes: list[tuple[int, int]] | None = None
    title: str = "Pygame Window"
    clean_color: tuple[int, int, int] = (0, 0, 0)
    target_fps: int = 0
    depth: int = 0
    vsync: int = 0
    start_fullscreen: bool = False
    can_fullscreen: bool = True
    can_resize: bool = True


class Window(Protocol):
    """Window Protocol"""

    display: pygame.Surface
    config: WindowConfig

    def __init__(self, config: WindowConfig) -> None:
        ...

    def render(self):
        """Render to the screen"""

    def update_win_size(self, size_option: int):
        """Update window size with if the option is avalible in disktop sizes"""

    def toggle_fullscreen(self):
        """Turn on/off fullscreen"""

    def set_title(self, title="Pygame Window", icontitle: str | None = None):
        """Set window title"""

    def clean(self, bg_color: pygame.Color):
        """fills the screen/display with the given color"""

    def quit(self):
        """Quit pygame and exit"""


CallableScene = NamedTuple(
    "CallableScene", [("scene_class", "Scene2D"), ("kwargs", "dict[str, Any]")]
)


class Game(Protocol):
    """General class that represent the game"""

    window: Window
    scenes: dict[str, CallableScene]

    def __init__(self, window: Window) -> None:
        ...

    def change_scene(self, name: str):
        """Method to change scenes if name is avalible in scenes"""

    def run(self):
        """Run the main game loop"""


class Scene2D(ABC):
    """Abstract Class representing a single game scene"""

    game: Game

    def __init__(self, game: Game) -> None:
        ...

    def update(self, dt: float):
        """For updating stuff"""

    def render(self):
        """For rendering stuff"""



