"""Event handling"""

import pygame

from .keyboard import Keyboard
from .window import Window


class EventHandler:
    """Class for hangling all the events"""

    def loop(self, window: Window, keyboard: Keyboard):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    window.quit()
                case pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        window.toggle_fullscreen()
            keyboard.handle_event(event)
