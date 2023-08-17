"""Event handling"""

import pygame

from .window import Window


class EventHandler:
    """Class for hangling all the events"""

    def loop(self, window: Window):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    window.quit()
                case pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        window.toggle_fullscreen()
