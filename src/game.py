"""Game"""
import pygame

from .window import Window


class Game:
    """General class that represent the game"""

    def __init__(self, window: Window) -> None:
        self.window = window

    def run(self):
        """Run the main game loop"""

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.window.quit()
                    case pygame.KEYDOWN:
                        if event.key == pygame.K_F11:
                            self.window.toggle_fullscreen()

            self.window.clean((30, 30, 30))
            self.window.render()
