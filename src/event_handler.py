"""Event handling"""

import pygame

from .config import Window
from .inputs import Keyboard, Mouse


class EventHandler:
    """Class for hangling all the events"""

    def loop(self, window: Window, keyboard: Keyboard, mouse: Mouse):
        """Event loop"""

        for event in pygame.event.get():
            keyboard.handle_event(event)
            mouse.handle_event(event)
            match event.type:
                case pygame.QUIT:
                    window.quit()
