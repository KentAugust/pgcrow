"""## Mouse handling"""

from dataclasses import dataclass
from typing import Any, Optional

import pygame

from ..timers import TimeClock
from .general import InputKey


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


@dataclass
class Wheel:
    """Wheel dataclass"""

    flipped: bool
    x: int
    y: int
    precise_x: float
    precise_y: float
    touch: bool
    window: None


class Mouse:
    """Class for handling mouse events"""

    def __init__(self):
        self._buttons: dict[InputKey, Button] = {}
        self.motion: Motion | None = None
        self.wheel: Wheel | None = None
        self.timer = TimeClock()

    def handle_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                start_time = self.timer.seconds
                start_frame = pygame.time.get_ticks()
                self._buttons[event.button] = Button(
                    pos=event.pos,
                    number=event.button,
                    touch=event.touch,
                    window=event.window,
                    pressed=True,
                    start_time=start_time,
                    start_frame=start_frame,
                    end_time=None,
                    end_frame=None,
                )
            case pygame.MOUSEBUTTONUP:
                self._buttons[event.button].pressed = False
                self._buttons[event.button].end_time = self.timer.seconds
                self._buttons[event.button].end_frame = pygame.time.get_ticks()
            case pygame.MOUSEMOTION:
                self.motion = Motion(
                    event.pos, event.rel, event.buttons, event.touch, event.window
                )
            case pygame.MOUSEWHEEL:
                self.wheel = Wheel(
                    event.flipped,
                    event.x,
                    event.y,
                    event.precise_x,
                    event.precise_y,
                    event.touch,
                    event.window,
                )

    def get_input_data(self, key: InputKey) -> Optional[Button]:
        """Get data of an specific input"""
        return self._buttons[key] if key in self._buttons else None

    def is_pressed(self, key: InputKey) -> bool:
        """Check if input key is pressed"""
        return k.pressed if (k := self.get_input_data(key)) else False

    def just_pressed(self, key: InputKey) -> bool:
        """Check if input key is pressed in this exact frame"""
        return self.hold_frames(key) == 0

    def just_released(self, key: InputKey) -> bool:
        """Check if input key stop being pressed in this exact frame"""
        return self.frames_since_release(key) == 0

    def press_time(self, key: InputKey) -> Optional[float]:
        """Get the time that an input key was pressed"""
        return k.start_time if (k := self.get_input_data(key)) else None

    def press_frame(self, key: InputKey) -> Optional[int]:
        """Get the frame that an input key was pressed"""
        return k.start_frame if (k := self.get_input_data(key)) else None

    def hold_time(self, key: InputKey) -> Optional[float]:
        """Return how long an input key is being pressed"""
        return (
            self.timer.seconds - k.start_time
            if (k := self.get_input_data(key))
            else None
        )

    def hold_frames(self, key: InputKey) -> Optional[int]:
        """Return how many frames an input key is being pressed"""
        return (
            pygame.time.get_ticks() - k.start_frame
            if (k := self.get_input_data(key))
            else None
        )

    def release_time(self, key: InputKey) -> Optional[float]:
        """Return the time an input key stop being pressed"""
        return k.end_time if (k := self.get_input_data(key)) else None

    def release_frame(self, key: InputKey) -> Optional[int]:
        """Return the frame an input key stop being pressed"""
        return k.end_frame if (k := self.get_input_data(key)) else None

    def time_since_release(self, key: InputKey) -> Optional[float]:
        """Return how long an input key stop pressed"""
        return self.timer.seconds - t if (t := self.release_time(key)) else None

    def frames_since_release(self, key: InputKey) -> Optional[int]:
        """Return how many frames an input key stop pressed"""
        return pygame.time.get_ticks() - t if (t := self.release_frame(key)) else None

    def get_pressed(self) -> list[Button]:
        """Get all buttons being pressed"""
        return [k for k in self._buttons.values() if k.pressed]

    @staticmethod
    def get_pos() -> tuple[int, int]:
        """Get the mouse position"""
        return pygame.mouse.get_pos()

    @staticmethod
    def get_pos_scaled(
        screen_size: tuple[int, int], display_size: tuple[int, int]
    ) -> tuple[float, float]:
        """Get the mouse position scaled"""
        mouse_pos = pygame.mouse.get_pos()
        return (
            mouse_pos[0] / screen_size[0] * display_size[0],
            mouse_pos[1] / screen_size[1] * display_size[1],
        )

    @staticmethod
    def get_visible() -> bool:
        """Get the current visibility state of the mouse cursor"""
        return pygame.mouse.get_visible()

    @staticmethod
    def get_focused() -> bool:
        """Check if the display is receiving mouse input"""
        return pygame.mouse.get_focused()

    @staticmethod
    def set_pos(pos: tuple[int, int]):
        """Set the mouse cursor position"""
        return pygame.mouse.set_pos(pos)

    @staticmethod
    def set_visible(visible: bool) -> int:
        """Hide or show the mouse cursor"""
        return pygame.mouse.set_visible(visible)

    def __getitem__(self, key: InputKey) -> Button:
        return self.get_input_data(key)
