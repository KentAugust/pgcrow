"""## Window
Window module for handling differents type of window"""

import sys
import pygame

from .config import WindowConfig


class Window:
    """Window class"""

    def __init__(
        self,
        config: WindowConfig,
        title="Pygame Window",
        init_fullscreen=False,
        window_sizes: list[tuple[int, int]] | None = None,
    ) -> None:
        self.config = config
        self.is_fullscreen = init_fullscreen and self.config.can_fullscreen

        if not pygame.get_init():
            pygame.init()

        # init desktop sizes
        self.desktop_sizes = pygame.display.get_desktop_sizes()
        window_sizes = window_sizes if window_sizes else []
        for size in sorted(window_sizes, reverse=True):
            if self.config.window_size not in set(self.desktop_sizes):
                self.desktop_sizes.append(size)
        if self.config.window_size not in set(self.desktop_sizes):
            self.desktop_sizes.append(self.config.window_size)
        self.desktop_sizes = tuple(self.desktop_sizes)

        self.update_win_size(
            self.desktop_sizes.index(self.config.window_size)
        )  # init window
        self.set_title(title)

        # init display surface
        self.display = pygame.transform.scale_by(
            pygame.Surface(self.config.display_size), 1 / self.config.scale_factor
        )
        self.clock: pygame.Clock = pygame.Clock()

    def render(self):
        """Render to the screen"""

        self.__win_screen.blit(
            pygame.transform.scale(self.display, self.__win_screen.get_size()), (0, 0)
        )
        pygame.display.update()
        self.clock.tick(self.config.target_fps)

    def update_win_size(self, size_option: int):
        """Update window size with if the option is avalible in disktop sizes"""

        try:
            size = self.desktop_sizes[size_option]
        except IndexError:
            size = self.config.window_size

        try:
            if size == pygame.display.get_window_size():
                return
        except pygame.error:
            size = self.config.window_size

        if size_option == 0:
            if self.config.can_fullscreen:
                if not self.is_fullscreen:
                    self.__win_screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                self.is_fullscreen = not self.is_fullscreen
                self.current_win_size = pygame.display.get_window_size()
            return

        self.is_fullscreen = False if self.is_fullscreen else False

        self.__win_screen = pygame.display.set_mode(size)
        self.current_win_size = pygame.display.get_window_size()

    def toggle_fullscreen(self):
        """Turn on/off fullscreen"""

        if not self.is_fullscreen:
            self.update_win_size(0)
        else:
            option = self.desktop_sizes.index(self.config.window_size)
            self.update_win_size(option)
            return

    def set_title(self, title="Pygame Window", icontitle: str | None = None):
        """Set window title"""

        if icontitle:
            pygame.display.set_caption(title, icontitle)
        else:
            pygame.display.set_caption(title)

    def clean(self, bg_color: pygame.Color):
        """fills the display with the given color"""

        self.display.fill(bg_color)

    def quit(self):
        """Quit pygame and exit"""
        pygame.quit()
        sys.exit()
