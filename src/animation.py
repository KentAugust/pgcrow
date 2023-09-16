"""Animation Module"""

import pygame
from pygame.transform import flip

from .consts import FrameData
from .timers import Chronometer


class Animation:  # pylint: disable=R0902
    """Class for hangling animations"""

    def __init__(self, animation_data: list[FrameData], loop: bool = False):
        self._animation_data = animation_data
        self.loop = loop
        self.ended = False
        self.paused = False
        self.frame = 0
        self._flip = [False, False]
        self._current_frame = 0
        self._chronometer = Chronometer()

    def play(
        self, dt: float, flip_x: bool = False, flip_y: bool = False
    ) -> pygame.Surface:
        """Updates the current frame"""
        if not self.ended and not self.paused:
            self._chronometer.update(dt)

        # update animation frame
        if (
            self._chronometer.current_time
            >= self._animation_data[self._current_frame][1]
        ):
            self.frame += 1
            if not self.loop and self.frame >= len(self._animation_data):
                self.frame = len(self._animation_data) - 1
                self.ended = True
            self._current_frame = self.frame % len(self._animation_data)
            self._chronometer.reset()

        self._flip = [flip_x, flip_y]

    def pause(self) -> bool:
        """Pause the animation"""
        self.paused = not self.paused
        return self.paused

    def stop(self):
        """Restart the animation"""
        self._chronometer.reset()
        self.frame = 0
        self._current_frame = 0
        self.ended = False

    def copy(self) -> "Animation":
        """Return a copy of Animation"""
        return Animation(self._animation_data, self.loop)

    @property
    def image(self) -> pygame.Surface:
        """Get the current frame surface"""
        return flip(
            self._animation_data[self._current_frame][0], self._flip[0], self._flip[1]
        )

    @property
    def animation_data(self) -> list[FrameData]:
        """Get all frames data"""
        return self._animation_data
