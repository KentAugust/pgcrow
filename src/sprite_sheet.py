"""Sprite sheet module"""

import pygame


class SpriteSheet:
    """Class to handle sprite sheets"""

    def __init__(
        self,
        img: pygame.Surface,
        horizontal_frames: int = 1,
        vertical_frames: int = 1,
        frame: tuple[int, int] = (0, 0),
    ) -> None:
        self._img = img

        # number of frames horizontally and vertically
        self._h_frames = max(1, min(abs(horizontal_frames), self._img.get_width()))
        self._v_frames = max(1, min(abs(vertical_frames), self._img.get_height()))

        # frame size
        self._frame_widht = self._img.get_width() // self._h_frames
        self._frame_height = self._img.get_height() // self._v_frames

        # number of total frames
        self._total_frames = (
            self._img.get_width()
            // self._frame_widht
            * self._img.get_height()
            // self._frame_height
        )
        # start frame
        self._frame = (
            frame[0] % self._h_frames,
            frame[1] % self._v_frames,
        )

    @property
    def image(self):
        """Return currente frame image"""
        return self._img.subsurface(
            self._frame[0] * self._frame_widht,
            self._frame[1] * self._frame_height,
            self._frame_widht,
            self._frame_height,
        )

    @property
    def frame(self) -> tuple[int, int]:
        """Get currente frame"""
        return self._frame

    @frame.setter
    def frame(self, value: tuple[int, int]):
        """Sets new frame"""
        self._frame = (value[0] % self._h_frames, value[1] % self._v_frames)

    @property
    def total_frames(self) -> int:
        """Return number of total frames"""
        return self._total_frames

    @property
    def horizontal_frames(self) -> int:
        """Return number of horizontal frames"""
        return self._h_frames

    @property
    def vertical_frames(self) -> int:
        """Return number of vertical frames"""
        return self._v_frames
