"""## Scene 2D"""

import pygame

from .game import Game


class Scene2D:
    """Class representing a single game scene"""

    def __init__(self, game: Game) -> None:
        self.game = game

    def update(self, dt: float):
        """For updating stuff"""
        if self.game.keyboard.pressed_this_frame(pygame.K_F11):
            self.game.window.toggle_fullscreen()

    def render(self):
        """For rendering stuff"""
