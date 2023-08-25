"""Config
module for setting different type of configuration needed for other classes"""

from dataclasses import dataclass
from typing import Any, NamedTuple, Protocol

import pygame


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

    def __init__(self, window: Window) -> None:
        ...

    def run(self):
        """Run the main game loop"""


class SceneManager(Protocol):
    """Class for hanglind scenes"""

    actual_scene: "Scene2D"
    actual_scene_name: str

    def __init__(
        self, game: Game, initial_scene: CallableScene, initial_scene_name: str
    ) -> None:
        ...

    def add_scene(self, name: str, scene: CallableScene):
        """Adds new scene to scenes"""

    def remove_scene(self, name: str):
        """Removes scene from scenes"""

    def change_scene(self, name: str):
        """Method to change scenes if name is avalible in scenes"""

    def scenes_names(self) -> set:
        "Get all scenes names"


class Scene2D(Protocol):
    """Abstract Class representing a single game scene"""

    game: Game

    def __init__(self, game: Game) -> None:
        ...

    def set_scene_manager(self, scene_manager: SceneManager):
        """Set scene manager"""

    def update(self, dt: float):
        """For updating stuff"""

    def render(self):
        """For rendering stuff"""
