"""## Mouse handling"""

from dataclasses import dataclass
from typing import Any, Optional

import pygame

from ..timers import TimeClock


@dataclass
class Button:
    """Button dataclass"""

    pos: tuple[int, int]
    number: int
    touch: str
    window: Any
    pressed: bool
    start_time: float
    start_frame: int
    end_time: Optional[float]
    end_frame: Optional[int]


@dataclass
class Motion:
    """Motion dataclass"""

    pos: tuple[int, int]
    rel: tuple[int, int]
    buttons: tuple[int, int, int]
    touch: bool
    window: Any


class Mouse:
    """Class for handling mouse events"""

    def __init__(self):
        self.buttons: dict[int, Button] = {}
        self.motion: Motion | None = None
        self.timer = TimeClock()

    def handle_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                start_time = self.timer.seconds
                start_frame = pygame.time.get_ticks()
                self.buttons[event.button] = Button(
                    pos = event.pos,
                    number = event.button,
                    touch = event.touch,
                    window = event.window,
                    pressed=True,
                    start_time=start_time,
                    start_frame=start_frame,
                    end_time=None,
                    end_frame=None,
                )
            case pygame.MOUSEBUTTONUP:
                self.buttons[event.button].pressed = False
                self.buttons[event.button].end_time = self.timer.seconds
                self.buttons[event.button].end_frame = pygame.time.get_ticks()
            case pygame.MOUSEMOTION:
                self.motion = Motion(event.pos, event.rel, event.buttons, event.touch, event.window)
            case pygame.MOUSEWHEEL:
                # TODO <Event(1027-MouseWheel {'flipped': False, 'x': 0, 'y': 1, 'precise_x': 0.0, 'precise_y': 1.0, 'touch': False, 'window': None})>
                pass

    @staticmethod
    def get_pos() -> tuple[int, int]:
        return pygame.mouse.get_pos()

    @staticmethod
    def get_pos_scaled(screen_size: tuple[int, int], display_size: tuple[int, int]) -> tuple[float, float]:
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos[0]/screen_size[0] * display_size[0], mouse_pos[1]/screen_size[1] * display_size[1]

    @staticmethod
    def get_visible() -> bool:
        return pygame.mouse.get_visible()

    @staticmethod
    def get_focused() -> bool:
        return pygame.mouse.get_focused()

    @staticmethod
    def set_pos(pos: tuple[int, int]):
        return pygame.mouse.set_pos(pos)

    @staticmethod
    def set_visible(visible: bool) -> int:
        return pygame.mouse.set_visible(visible)

    def __getitem__(self, key: int) -> Button:
        return self.button(key)

    def get_pressed(self) -> list[Button]:
        return [k for k in self.buttons.values() if k.pressed]

    def button(self, key: int) -> Optional[Button]:
        return self.buttons[key] if key in self.buttons else None

    def is_pressed(self, key: int) -> bool:
        return k.pressed if (k := self.button(key)) else False

    def press_time(self, key: int) -> Optional[float]:
        return k.start_time if (k := self.button(key)) else None

    def press_frame(self, key: int) -> Optional[int]:
        return k.start_frame if (k := self.button(key)) else None

    def frames_since_press(self, key: int) -> Optional[int]:
        return pygame.time.get_ticks() - k.start_frame if (k := self.button(key)) else None

    def pressed_this_frame(self, key: int) -> bool:
        return self.frames_since_press(key) == 0

    def is_held(self, key: int) -> bool:
        return k.pressed if (k := self.button(key)) else False

    def hold_time(self, key: int) -> Optional[float]:
        return self.timer.seconds - k.start_time if (k := self.button(key)) else None

    def hold_frames(self, key: int) -> Optional[int]:
        return pygame.time.get_ticks() - k.start_frame if (k := self.button(key)) else None

    def release_time(self, key: int) -> Optional[float]:
        return k.end_time if (k := self.button(key)) else None

    def time_since_release(self, key: int) -> Optional[float]:
        return self.timer.seconds - t if (t := self.release_time(key)) else None

    def release_frame(self, key: int) -> Optional[int]:
        return k.end_frame if (k := self.button(key)) else None

    def frames_since_release(self, key: int) -> Optional[int]:
        return pygame.time.get_ticks() - t if (t := self.release_frame(key)) else None

    def released_this_frame(self, key: int) -> bool:
        return self.frames_since_release(key) == 0
