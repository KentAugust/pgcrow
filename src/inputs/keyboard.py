"""## Keyboard handling"""

from dataclasses import dataclass
from typing import Optional

import pygame

from ..timers import TimeClock
from .general import InputKey


@dataclass
class KeyboardKey:
    """KeyboardKey dataclass"""

    key: int
    name: str
    pressed: bool
    start_time: float
    start_frame: int
    end_time: Optional[float]
    end_frame: Optional[int]


class Keyboard:
    """Class for handling keys events"""

    def __init__(self):
        self._keys: dict[InputKey, KeyboardKey] = {}

    def handle_event(self, event: pygame.Event) -> None:
        """Handle a single event"""
        if event.type == pygame.KEYDOWN:
            start_time = TimeClock().seconds()
            start_frame = pygame.time.get_ticks()
            self._keys[event.key] = KeyboardKey(
                key=event.key,
                name=pygame.key.name(event.key),
                pressed=True,
                start_time=start_time,
                start_frame=start_frame,
                end_time=None,
                end_frame=None,
            )
        elif event.type == pygame.KEYUP:
            self._keys[event.key].pressed = False
            self._keys[event.key].end_time = TimeClock().seconds()
            self._keys[event.key].end_frame = pygame.time.get_ticks()

    def get_input_data(self, key: InputKey) -> Optional[KeyboardKey]:
        """Get data of an specific key"""
        return self._keys[key] if key in self._keys else None

    def is_pressed(self, key: InputKey) -> bool:
        """Check if key is pressed"""
        return k.pressed if (k := self.get_input_data(key)) else False

    def just_pressed(self, key: InputKey) -> bool:
        """Check if key is pressed in this exact frame"""
        return self.frames_since_press(key) == 0

    def just_released(self, key: InputKey) -> bool:
        """Check if key stop being pressed in this exact frame"""
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
            TimeClock().seconds() - k.start_time
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
        return TimeClock().seconds() - t if (t := self.release_time(key)) else None

    def frames_since_release(self, key: InputKey) -> Optional[int]:
        """Return how many frames an input key stop pressed"""
        return pygame.time.get_ticks() - t if (t := self.release_frame(key)) else None

    def get_pressed(self) -> list[KeyboardKey]:
        """Get all keys being pressed"""
        return [k for k in self._keys.values() if k.pressed]

    def __getitem__(self, key: InputKey) -> Optional[KeyboardKey]:
        return self.get_input_data(key)
