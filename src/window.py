"""## Window
Window module for handling differents type of window"""

from typing import Self

import pygame

from .config import WindowConfig


class WindowScreen:
    """Window class that blits on the screen"""

    def __init__(self, config: WindowConfig) -> None:
        self._const_flags = 0
        self._prev_size = config.window_size
        self._current_size = config.window_size
        self._win_screen = None
        self._is_fullscreen = False
        self._desktop_sizes = []
        self.config = config

    def init_screen(self) -> Self:
        """Initialize screen"""
        if not pygame.get_init():
            pygame.init()
            self._init_desktop_sizes()
            size_index = self._desktop_sizes.index(self.config.window_size)
            self.change_size(self._desktop_sizes[size_index])
            self._is_fullscreen = size_index == 0
        return self

    def update_display(self, _offset: tuple[int, int] = (0, 0)):
        """Render to the screen"""
        pygame.display.update()

    def change_size(self, size: tuple[int, int], fullscreen=False) -> bool:
        """Update window size if it can"""
        if not self.config.can_resize and self._win_screen is not None:
            if not self.config.can_fullscreen or (
                self.config.can_fullscreen
                and (self.config.window_size != size != self._desktop_sizes[0])
            ):
                return False

        flags = self._const_flags
        if fullscreen:
            flags = self._const_flags | pygame.FULLSCREEN
        self._prev_size = self._current_size
        self._win_screen = pygame.display.set_mode(
            size=size, flags=flags, depth=self.config.depth, vsync=self.config.vsync
        )
        self._current_size = size
        return True

    def toggle_fullscreen(self) -> bool:
        """Turn on/off fullscreen"""
        if not self.config.can_fullscreen:
            return False
        if self._is_fullscreen:
            has_changed = self.change_size(self._prev_size)
        else:
            has_changed = self.change_size(self._desktop_sizes[0], True)
        if has_changed:
            self._is_fullscreen = not self._is_fullscreen
        return has_changed

    def clean(self, bg_color: pygame.Color):
        """fills the screen/display with the given color"""
        self._win_screen.fill(bg_color)
        self.display.fill(bg_color)

    def _init_desktop_sizes(self):
        self._desktop_sizes = pygame.display.get_desktop_sizes()
        if not self.config.avalible_window_sizes:
            self.config.avalible_window_sizes = []
        for size in sorted(self.config.avalible_window_sizes, reverse=True):
            if size not in set(self._desktop_sizes):
                self._desktop_sizes.append(size)
        if self.config.window_size not in set(self._desktop_sizes):
            self._desktop_sizes.append(self.config.window_size)
        self._desktop_sizes = tuple(
            sorted(self._desktop_sizes, key=lambda s: s[0], reverse=True)
        )

    @property
    def current_size(self):
        """Get current size"""
        return self._current_size

    @property
    def desktop_sizes(self):
        """Get a list of avalible desktop sizes"""
        return self._desktop_sizes

    @property
    def is_fullscreen(self):
        """Get if window is fullscreen"""
        return self._is_fullscreen

    @property
    def display(self):
        """Returns the screen surface"""
        return self._win_screen

    @property
    def screen(self):
        """Returns the screen surface"""
        return self._win_screen


class WindowDisplay(WindowScreen):
    """Window class that blits on a intermediate display"""

    def __init__(self, config: WindowConfig) -> None:
        super().__init__(config)
        match config.scale_funtion:
            case "smooth":
                self.scale_funtion = pygame.transform.smoothscale
            case _:
                self.scale_funtion = pygame.transform.scale

    def init_screen(self) -> Self:
        """Initialize screen"""
        super().init_screen()
        screen_size = self._win_screen.get_size()
        self._display = pygame.transform.scale_by(
            pygame.Surface(screen_size), 1 / self.config.scale_factor
        )
        return self

    def update_display(self, offset: tuple[int, int] = (0, 0)):
        """Render to the screen"""
        self._win_screen.blit(
            self.scale_funtion(self._display, self._win_screen.get_size()), offset
        )
        pygame.display.update()

    @property
    def display(self):
        """Returns the display surface"""
        return self._display


class WindowScreenGl(WindowScreen):
    """Window class that blits on the screen. Set pygame.OPENGL | pygame.DOUBLEBUF flags"""

    def __init__(self, config: WindowConfig) -> None:
        super().__init__(config)
        self._const_flags = pygame.DOUBLEBUF | pygame.OPENGL
        self._screen_surf = pygame.Surface(self.config.window_size)

    def init_screen(self) -> Self:
        """Initialize screen"""
        if not pygame.get_init():
            super().init_screen()
            self._screen_surf = pygame.Surface(self._win_screen.get_size())
        return self

    def update_display(self, _offset: tuple[int, int] = (0, 0)):
        """Render to the screen not implemented, manually use pygame.flip instead"""

    def change_size(self, size: tuple[int, int], fullscreen=False) -> bool:
        if size == self._desktop_sizes[0]:
            return self.toggle_fullscreen()
        return super().change_size(size, fullscreen)

    def toggle_fullscreen(self):
        """Turn on/off fullscreen"""
        was_fullscreen = self._is_fullscreen
        pygame.display.toggle_fullscreen()
        self._is_fullscreen = pygame.display.is_fullscreen()
        
        self._current_size = self._desktop_sizes[0] if self._is_fullscreen else self._prev_size

        if self._is_fullscreen != was_fullscreen:
            self._screen_surf = pygame.Surface(self._win_screen.get_size())
        return self._is_fullscreen != was_fullscreen

    @property
    def display(self):
        """Returns the screen surface"""
        return self._screen_surf

    @property
    def screen(self):
        """Returns the screen surface"""
        return self._screen_surf


class WindowDisplayGl(WindowScreenGl):
    def __init__(self, config: WindowConfig) -> None:
        super().__init__(config)
        match config.scale_funtion:
            case "smooth":
                self.scale_funtion = pygame.transform.smoothscale
            case _:
                self.scale_funtion = pygame.transform.scale

    def init_screen(self) -> Self:
        """Initialize screen"""
        super().init_screen()
        screen_size = self._screen_surf.get_size()
        self._display = pygame.transform.scale_by(
            pygame.Surface(screen_size), 1 / self.config.scale_factor
        )
        return self
    
    def update_display(self, offset: tuple[int, int] = (0, 0)):
        """Render to the screen partially implemented, manually use pygame.flip instead"""
        self._screen_surf.blit(
            self.scale_funtion(self._display, self._screen_surf.get_size()), offset
        )

    @property
    def display(self):
        """Returns the screen surface"""
        return self._display