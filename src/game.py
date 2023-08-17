"""Game"""
import pygame

from .event_handler import EventHandler
from .window import Window


class Game:
    """General class that represent the game"""

    def __init__(self, window: Window) -> None:
        self.window = window
        self.event_handler = EventHandler()

    def run(self):
        """Run the main game loop"""

        while True:
            self.event_handler.loop(self.window)
            self.window.clean((30, 30, 30))
            self.window.render()
