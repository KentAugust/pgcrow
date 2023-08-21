"""## Scene 2D"""

import pygame

from .inputs import Keyboard, Mouse
from .window import Window


class Scene2D:
    """Class representing a single game scene"""

    def __init__(self, game) -> None:
        self.game = game
        self.game.event_handler.loop = self.handle_events

    def handle_events(self, window: Window, keyboard: Keyboard, mouse: Mouse):
        """Custom event handling method"""

        for event in pygame.event.get():
            keyboard.handle_event(event)
            mouse.handle_event(event)
            match event.type:
                case pygame.QUIT:
                    window.quit()

    def update(self, dt: float):
        """For updating stuff"""
        if self.game.keyboard.pressed_this_frame(pygame.K_F11):
            self.game.window.toggle_fullscreen()

    def render(self):
        """For rendering stuff"""
