"""## Scene 2D"""

import pygame

from .config import Game, SceneManager


class Scene2D:
    """Class representing a single game scene"""

    def __init__(self, game: Game) -> None:
        self.game = game
        self.scene_manager = None

    def set_scene_manager(self, scene_manager: SceneManager):
        """Set scene manager"""

        self.scene_manager = scene_manager

    def on_enter(self, dt: float) -> bool:
        """Ativate when enter the scene and return True when finish"""

        return True

    def on_exit(self, dt: float) -> bool:
        """Ativate when exit the scene and return True when finish"""

        return True

    def update(self, dt: float):
        """For updating stuff"""
        if self.game.keyboard.pressed_this_frame(pygame.K_F11):
            self.game.window.toggle_fullscreen()

    def render(self):
        """For rendering stuff"""
