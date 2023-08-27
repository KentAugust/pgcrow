"""Event handling"""

import pygame

from .config import Game


class EventHandler:
    """Class for hangling all the events"""

    def __init__(self, game: Game) -> None:
        self.game = game

    def loop(self):
        """Event loop"""

        for event in pygame.event.get():
            self.game.keyboard.handle_event(event)
            self.game.mouse.handle_event(event)
            match event.type:
                case pygame.QUIT:
                    self.game.quit()
