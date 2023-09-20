"""Animation Module"""

import pygame
from pygame.transform import flip

from .consts import FrameData
from .timers import Chronometer


class Animation:  # pylint: disable=R0902
    """Base class for hangling animations"""

    def __init__(self, length: float = 1, fps: int = 24, loop: bool = False):
        self.loop = loop
        self.has_ended = False
        self.is_paused = False
        self._length = max(1, length)
        self._current_frame = 0
        self._fps = max(1, fps)
        self._total_frames = round(self._fps * self._length)
        self.frame_length = self._length / self._total_frames / 2
        self._frame = 0
        self._timer = Chronometer()
        self._current_time = 0

    def play(self, dt: float):
        """Updates the current frame"""
        if not self.has_ended and not self.is_paused:
            self._timer.update(dt)
            self._current_time += self.dt

        # update animation frame
        if self._timer.current_time >= self.frame_length:
            self._current_frame += 1
            if not self.loop and self._current_frame >= self._total_frames:
                self._current_frame = self._total_frames - 1
                self.has_ended = True
            self._frame = self._current_frame % self._total_frames
            self._timer.reset()

    def pause(self) -> bool:
        """Pause the animation"""
        self.is_paused = not self.is_paused
        return self.is_paused

    def stop(self):
        """Restart the animation"""
        self._timer.reset()
        self._current_frame = 0
        self._frame = 0
        self.has_ended = False

    def copy(self) -> "Animation":
        """Return a copy of Animation"""
        return Animation(self._length, self._fps, self.loop)

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    def length(self, value: float):
        self._length = max(1, value)
        self._total_frames = round(self._fps * self._length)

    @property
    def frame(self) -> int:
        return self._frame

    @property
    def current_frame(self) -> int:
        return self._current_frame
    
    @property
    def current_time(self) -> float:
        return self._current_time


class SpriteAnimation(Animation):  # pylint: disable=R0902
    """Class for hangling sprite animations"""

    def __init__(self, animation_data: list[FrameData], loop: bool = False):
        lenght = sum(frame_data[1] for frame_data in animation_data)
        super().__init__(lenght, len(animation_data)*lenght, loop)
        self._animation_data = animation_data
        self._total_frames = len(animation_data)
        self.frame_length = self._animation_data[0][1]
        self._flip = [False, False]

    def play(self, dt: float, flip_x: bool = False, flip_y: bool = False):
        """Updates the current frame"""
        super().play(dt)
        self.frame_length = self._animation_data[self._frame][1]
        self._flip = [flip_x, flip_y]

    def pause(self) -> bool:
        """Pause the animation"""
        self.is_paused = not self.is_paused
        return self.is_paused

    def stop(self):
        """Restart the animation"""
        self._timer.reset()
        self._current_frame = 0
        self._frame = 0
        self.has_ended = False

    def copy(self) -> "Animation":
        """Return a copy of Animation"""
        return SpriteAnimation(self._animation_data, self.loop)

    @property
    def image(self) -> pygame.Surface:
        """Get the current frame surface"""
        return flip(self._animation_data[self._frame][0], self._flip[0], self._flip[1])

    @property
    def animation_data(self) -> list[FrameData]:
        """Get all frames data"""
        return self._animation_data
