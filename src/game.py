"""## Game"""

import sys

import pygame

from .config import GameConfig, Window
from .event_handler import EventHandler
from .inputs import Keyboard, Mouse
from .scene_manager import SceneManager
from .timers import Deltatimer


class Game:
    """General class that represent the game"""

    def __init__(
        self,
        config: GameConfig,
        window: Window,
    ) -> None:
        self.config = config
        self.window = window

        self.set_title(self.config.title)
        if self.config.start_fullscreen and self.window.config.can_fullscreen:
            self.window.toggle_fullscreen()

        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.event_handler = EventHandler(self)
        self.scene_manager = SceneManager(self)  # set main as an empty scene
        self.clock = pygame.Clock()
        self.deltatimer = Deltatimer()

    def run(self):
        """Run the main game loop"""

        while True:
            dt = self.deltatimer.get_dt()
            self.window.clean(self.config.clean_color)
            self.event_handler.loop()
            self.scene_manager.update(dt)
            self.scene_manager.actual_scene.render()
            self.window.update_display()
            self.clock.tick(self.config.target_fps)

    def set_title(self, title="Pygame Window", icontitle: str | None = None):
        """Set window title"""

        if icontitle:
            pygame.display.set_caption(title, icontitle)
        else:
            pygame.display.set_caption(title)

    def quit(self):
        """Quit pygame and exit"""
        pygame.quit()
        sys.exit()
