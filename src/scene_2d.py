"""## Scene 2D"""

import pygame

from .window import Window


class Scene2D:
    """Class representing a single game scene"""

    def __init__(self, game) -> None:
        self.game = game
        self.game.event_handler.loop = self.handle_events

    def handle_events(self, window: Window):
        """Custom event handling method"""

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    window.quit()
                case pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        window.toggle_fullscreen()

    def update(self, dt: float):
        """For updating stuff"""

    def render(self):
        """For rendering stuff"""
