"""Event handling"""

import pygame

from .config import Game


class EventHandler:
    """Class for hangling all the events"""

    def __init__(self, game: Game) -> None:
        self.game = game
        self._last_event = pygame.Event(pygame.NOEVENT)

    def _handle_event(self, event: pygame.Event):
        """Handle a single event"""
        self.game.keyboard.handle_event(event)
        self.game.mouse.handle_event(event)
        self._last_event = event
        match event.type:
            case pygame.QUIT:
                self.game.quit()

    def loop(self) -> bool:
        """Event loop"""
        for event in pygame.event.get():
            self._handle_event(event)
        return True

    def poll(self) -> bool:
        """Event poll"""
        event = pygame.event.poll()
        self._handle_event(event)
        if event == pygame.NOEVENT:
            return False
        return True

    def peek(self) -> bool:
        """Event peek"""
        if pygame.event.peek():
            return self.poll()
        return False

    @property
    def last_event(self):
        """last Event type"""
        return self._last_event
