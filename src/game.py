"""## Game"""

import sys

import pygame

from .config import GameConfig, Window
from .event_handler import EventHandler
from .inputs import Keyboard, Mouse
from .maths import Vec2
from .scene_manager import SceneManager
from .timers import Delta


class Game:  # pylint: disable=R0902
    """General class that represent the game"""

    def __init__(self, config: GameConfig, window: Window) -> None:
        self.config = config
        self.window = window
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.event_handler = EventHandler(self)
        self.scene_manager = SceneManager(self)  # set main as an empty scene
        self.clock = pygame.Clock()
        self.deltatimer = Delta()
        self.display_offset = Vec2()

    def run(self):
        """Run the main game loop"""
        self.window.init_screen()
        self.scene_manager.start_initial_scene()
        self.set_title(self.config.title)
        if self.config.start_fullscreen and self.window.config.can_fullscreen:
            self.window.toggle_fullscreen()

        while True:
            delta = self.deltatimer.get_delta()
            self.window.clean(self.config.clean_color)
            self.event_handler.loop()
            self.scene_manager.update(delta)
            self.scene_manager.render(self.window.display)
            update_funtion = self.window.get_update_function(self.display_offset)
            self.scene_manager.render_screen(self.window.screen)
            if update_funtion is not None: update_funtion()
            self.clock.tick(self.config.target_fps)

    def update_win_size(self, size_option: int) -> tuple[int, int]:
        """Update window size with if the option is avalible in disktop sizes"""
        size_option = max(0, min(size_option, len(self.window.desktop_sizes) - 1))
        size = self.window.desktop_sizes[size_option]
        if size_option == 0:
            self.window.toggle_fullscreen()
            return size
        self.window.change_size(size)
        return size

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
