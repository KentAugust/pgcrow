"""## Window
Window module for handling differents type of window"""

import sys

import pygame

from .config import WindowConfig


class WindowScreen:
    """Window class that blits on the screen"""

    def __init__(self, config: WindowConfig) -> None:
        self.config = config
        self.is_fullscreen = False
        if not pygame.get_init():
            pygame.init()

        # init desktop sizes
        self.desktop_sizes = pygame.display.get_desktop_sizes()
        if not self.config.avalible_window_sizes:
            self.config.avalible_window_sizes = []
        for size in sorted(self.config.avalible_window_sizes, reverse=True):
            if size not in set(self.desktop_sizes):
                self.desktop_sizes.append(size)
        if self.config.window_size not in set(self.desktop_sizes):
            self.desktop_sizes.append(self.config.window_size)
        self.desktop_sizes = tuple(sorted(self.desktop_sizes, key=lambda s: s[0], reverse=True))

        self._win_screen = None
        self.update_win_size(
            self.desktop_sizes.index(self.config.window_size)
        )  # init window

        self.is_fullscreen = self.desktop_sizes.index(self.config.window_size) == 0
        if self.config.start_fullscreen and self.config.can_fullscreen:
            self.toggle_fullscreen()
        self.set_title(self.config.title)

        self.clock: pygame.Clock = pygame.Clock()

    def render(self):
        """Render to the screen"""

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
            try:
                self._prev_size = pygame.display.get_window_size()
            except pygame.error:
                self._prev_size = size
            if self.config.can_fullscreen:
                if not self.is_fullscreen:
                    self._win_screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

                self.is_fullscreen = not self.is_fullscreen
                self.current_win_size = pygame.display.get_window_size()
            return

        if self.config.can_resize or self.is_fullscreen or self._win_screen is None:
            if self.is_fullscreen and not self.config.can_resize:
                size = self._prev_size
            self._win_screen = pygame.display.set_mode(size)
            self.current_win_size = pygame.display.get_window_size()
        self.is_fullscreen = False if self.is_fullscreen else False

    def toggle_fullscreen(self):
        """Turn on/off fullscreen"""

        if not self.is_fullscreen:
            self.update_win_size(0)
        else:
            option = self.desktop_sizes.index(self._prev_size)
            self.update_win_size(option)
            return

    def set_title(self, title="Pygame Window", icontitle: str | None = None):
        """Set window title"""

        if icontitle:
            pygame.display.set_caption(title, icontitle)
        else:
            pygame.display.set_caption(title)

    def clean(self, bg_color: pygame.Color):
        """fills the screen/display with the given color"""

        self.display.fill(bg_color)

    def quit(self):
        """Quit pygame and exit"""
        pygame.quit()
        sys.exit()

    @property
    def display(self):
        """Returns the screen surface"""

        return self._win_screen


class WindowDisplay(WindowScreen):
    """Window class that blits on a intermediate display"""

    def __init__(self, config: WindowConfig) -> None:
        super().__init__(config)
        # init display surface
        display_size = self.config.display_size
        if not display_size:
            display_size = self._win_screen.get_size()
        self.__display = pygame.transform.scale_by(
            pygame.Surface(display_size), 1 / self.config.scale_factor
        )

    def render(self):
        """Render to the screen"""

        self._win_screen.blit(
            pygame.transform.scale(self.__display, self._win_screen.get_size()), (0, 0)
        )
        pygame.display.update()
        self.clock.tick(self.config.target_fps)

    @property
    def display(self):
        """Returns the display surface"""

        return self.__display
