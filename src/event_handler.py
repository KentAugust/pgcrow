"""Event handling"""

import pygame

from .inputs import Keyboard, Mouse
from .window import Window


class EventHandler:
    """Class for hangling all the events"""

    def loop(self, window: Window, keyboard: Keyboard, mouse: Mouse):
        for event in pygame.event.get():
            keyboard.handle_event(event)
            mouse.handle_event(event)
            match event.type:
                case pygame.QUIT:
                    window.quit()
        if keyboard.pressed_this_frame(pygame.K_F11):
            window.toggle_fullscreen()
