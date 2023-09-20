"""Animation Module"""

import pygame
from pygame.transform import flip

from .consts import FrameData
from .timers import Chronometer


class Animation:  # pylint: disable=R0902
    """Base class for hangling animations"""

    def __init__(self, lenght: float, total_frames: int, loop: bool = False):
        self.loop = loop
        self.lenght = lenght
        self.ended = False
        self.paused = False
        self._current_frame = 0
        self._total_frames = total_frames
        self._frame_lenght = self.lenght / self._total_frames
        self._frame = 0
        self._chronometer = Chronometer()

    def play(self, dt: float):
        """Updates the current frame"""
        if not self.ended and not self.paused:
            self._chronometer.update(dt)

        # update animation frame
        if (
            self._chronometer.current_time
            >= self._frame_lenght
        ):
            self._current_frame += 1
            if not self.loop and self._current_frame >= self._total_frames:
                self._current_frame = self._total_frames - 1
                self.ended = True
            self._frame = self._current_frame % self._total_frames
            self._chronometer.reset()

    def pause(self) -> bool:
        """Pause the animation"""
        self.paused = not self.paused
        return self.paused

    def stop(self):
        """Restart the animation"""
        self._chronometer.reset()
        self._current_frame = 0
        self._frame = 0
        self.ended = False

    def copy(self) -> "Animation":
        """Return a copy of Animation"""
        return Animation(self._animation_data, self.loop)


class SpriteAnimation(Animation):  # pylint: disable=R0902
    """Class for hangling sprite animations"""

    def __init__(self, animation_data: list[FrameData], loop: bool = False):
        lenght = sum([frame_data[1] for frame_data in animation_data])
        super().__init__(lenght, len(animation_data), loop)
        self._animation_data = animation_data
        self._frame_lenght = self._animation_data[0][1]
        self._flip = [False, False]

    def play(
        self, dt: float, flip_x: bool = False, flip_y: bool = False
    ):
        """Updates the current frame"""
        super().play(dt)
        self._frame_lenght = self._animation_data[self._frame][1]
        self._flip = [flip_x, flip_y]

    def pause(self) -> bool:
        """Pause the animation"""
        self.paused = not self.paused
        return self.paused

    def stop(self):
        """Restart the animation"""
        self._chronometer.reset()
        self._current_frame = 0
        self._frame = 0
        self.ended = False

    def copy(self) -> "Animation":
        """Return a copy of Animation"""
        return SpriteAnimation(self._animation_data, self.loop)

    @property
    def image(self) -> pygame.Surface:
        """Get the current frame surface"""
        return flip(
            self._animation_data[self._frame][0], self._flip[0], self._flip[1]
        )

    @property
    def animation_data(self) -> list[FrameData]:
        """Get all frames data"""
        return self._animation_data
