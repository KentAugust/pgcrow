"""## Keyboard handling"""

from dataclasses import dataclass
from typing import Optional

import pygame

from ..timers import TimeClock


@dataclass
class Key:
    """Key dataclass"""

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
        self.keys = {}
        self.timer = TimeClock()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            start_time = self.timer.seconds
            start_frame = pygame.time.get_ticks()
            self.keys[event.key] = Key(
                key=event.key,
                name=pygame.key.name(event.key),
                pressed=True,
                start_time=start_time,
                start_frame=start_frame,
                end_time=None,
                end_frame=None,
            )
        elif event.type == pygame.KEYUP:
            self.keys[event.key].pressed = False
            self.keys[event.key].end_time = self.timer.seconds
            self.keys[event.key].end_frame = pygame.time.get_ticks()

    def __getitem__(self, key: int) -> Key:
        return self.key(key)

    def get_pressed(self) -> list[Key]:
        return [k for k in self.keys.values() if k.pressed]

    def key(self, key: int) -> Optional[Key]:
        return self.keys[key] if key in self.keys else None

    def is_pressed(self, key: int) -> bool:
        return k.pressed if (k := self.key(key)) else False

    def press_time(self, key: int) -> Optional[float]:
        return k.start_time if (k := self.key(key)) else None

    def press_frame(self, key: int) -> Optional[int]:
        return k.start_frame if (k := self.key(key)) else None

    def frames_since_press(self, key: int) -> Optional[int]:
        return pygame.time.get_ticks() - k.start_frame if (k := self.key(key)) else None

    def pressed_this_frame(self, key: int) -> bool:
        return self.frames_since_press(key) == 0

    def is_held(self, key: int) -> bool:
        return k.pressed if (k := self.key(key)) else False

    def hold_time(self, key: int) -> Optional[float]:
        return self.timer.seconds - k.start_time if (k := self.key(key)) else None

    def hold_frames(self, key: int) -> Optional[int]:
        return pygame.time.get_ticks() - k.start_frame if (k := self.key(key)) else None

    def release_time(self, key: int) -> Optional[float]:
        return k.end_time if (k := self.key(key)) else None

    def time_since_release(self, key: int) -> Optional[float]:
        return self.timer.seconds - t if (t := self.release_time(key)) else None

    def release_frame(self, key: int) -> Optional[int]:
        return k.end_frame if (k := self.key(key)) else None

    def frames_since_release(self, key: int) -> Optional[int]:
        return pygame.time.get_ticks() - t if (t := self.release_frame(key)) else None

    def released_this_frame(self, key: int) -> bool:
        return self.frames_since_release(key) == 0
