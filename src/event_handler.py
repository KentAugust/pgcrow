"""Event handling"""

from typing import Protocol

import pygame


class EventObserver(Protocol):
    """Represent a class that handle events"""

    def handle_event(self, event: pygame.Event):
        """Handle a single event"""


class EventHandler:
    """Class for hangling all the events"""

    def __init__(self) -> None:
        self._observers: list[EventObserver] = []
        self._last_event = pygame.Event(pygame.NOEVENT)

    def register(self, observer: EventObserver) -> bool:
        """Register a new observer; return True if registered successfully"""
        if hasattr(observer, EventObserver.handle_event.__name__):
            if not self.check_registered(observer):
                self._observers.append(observer)
                return True
        return False

    def deregister(self, observer: EventObserver) -> bool:
        """Deregister a specific observer; return True if deregistered successfully"""
        if self.check_registered(observer):
            index = self._observers.index(observer)
            self._observers.pop(index)
            return True
        return False

    def check_registered(self, observer: EventObserver) -> bool:
        """Check if a observer is registered"""
        return observer in self._observers

    def _send_event(self, event: pygame.Event):
        """Send a single event to all observers"""
        for observer in self._observers:
            observer.handle_event(event)
        self._last_event = event

    def loop(self) -> bool:
        """Event loop"""
        for event in pygame.event.get():
            self._send_event(event)
        return True

    def poll(self) -> bool:
        """Event poll"""
        event = pygame.event.poll()
        self._send_event(event)
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
