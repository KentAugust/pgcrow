"""Sprites module"""

import pygame


def load_image(
    path: str, alpha: bool = False, colorkey: tuple[int, int, int] | None = None
) -> pygame.Surface:
    """Load image file"""
    img = pygame.image.load(path)
    img = img.convert_alpha() if alpha else img.convert()
    if colorkey:
        img.set_colorkey(colorkey)
    return img

def clip(
    surf: pygame.Surface, x: int, y: int, width: int, height: int
) -> pygame.Surface:
    """Return a cropped surface"""
    handle_surf = surf.copy()
    clip_rect = pygame.Rect(x, y, width, height)
    handle_surf.set_clip(clip_rect)
    img = surf.subsurface(handle_surf.get_clip())
    return img

def swap_color(
    surf: pygame.Surface,
    old_color: tuple[int, int, int],
    new_color: tuple[int, int, int],
) -> pygame.Surface:
    """change a color of the surface"""
    img_copy = pygame.Surface(surf.get_size())
    img_copy.fill(new_color)
    surf.set_colorkey(old_color)
    img_copy.blit(surf, (0, 0))
    return img_copy


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
        self._frame_cord = (
            frame[0] % self._h_frames,
            frame[1] % self._v_frames,
        )

    @property
    def image(self):
        """Return sprite image"""
        return self._img

    @property
    def frame(self):
        """Return currente frame image"""
        return self._img.subsurface(
            self._frame_cord[0] * self._frame_widht,
            self._frame_cord[1] * self._frame_height,
            self._frame_widht,
            self._frame_height,
        )

    @property
    def frame_cord(self) -> tuple[int, int]:
        """Get currente frame cordinates"""
        return self._frame_cord

    def set_frame_cord(self, value: tuple[int, int]):
        """Sets new frame cordinates"""
        self._frame_cord = (value[0] % self._h_frames, value[1] % self._v_frames)

    @property
    def horizontal_cord(self) -> int:
        """Get current frame horizontal cordinate"""
        return self._frame_cord[0]

    @horizontal_cord.setter
    def horizontal_cord(self, value: int):
        """Sets new frame horizontal cordinate"""
        self._frame_cord = (value % self._h_frames, self._frame_cord[1])

    @property
    def vertical_cord(self) -> int:
        """Get current frame vertical cordinate"""
        return self._frame_cord[1]

    @vertical_cord.setter
    def vertical_cord(self, value: int):
        """Sets new frame vertical cordinate"""
        self._frame_cord = (self._frame_cord[0], value % self._v_frames)

    @property
    def total_frames(self) -> int:
        """Return number of total frames"""
        return self._total_frames

    @property
    def horizontal_len(self) -> int:
        """Return number of horizontal frames"""
        return self._h_frames

    @property
    def vertical_len(self) -> int:
        """Return number of vertical frames"""
        return self._v_frames

    def __len__(self) -> int:
        """Return number of total frames"""
        return self._total_frames

    def __getitem__(self, key: tuple[int, int]):
        """Return currente frame image"""
        return self._img.subsurface(
            (key[0] % self._h_frames) * self._frame_widht,
            (key[1] % self._v_frames) * self._frame_height,
            self._frame_widht,
            self._frame_height,
        )


class TileSet(SpriteSheet):
    """Class to handle tilesets"""

    def __init__(self, img: pygame.Surface, tile_size: int) -> None:
        super().__init__(
            img, img.get_width() // tile_size, img.get_height() // tile_size
        )
        self._tiles_cords = []
        for vertical in range(self._v_frames):
            for horizontal in range(self._h_frames):
                cord = (horizontal, vertical)

                # check is the tile is empty
                if self._is_empty(
                    self._img.subsurface(
                        cord[0] * self._frame_widht,
                        cord[1] * self._frame_height,
                        self._frame_widht,
                        self._frame_height,
                    )
                ):
                    continue
                self._tiles_cords.append(cord)

    def _is_empty(self, surf: pygame.Surface) -> bool:
        """Check if the tile is completly transparent"""
        for row in range(surf.get_height()):
            for col in range(surf.get_width()):
                if surf.get_at((col, row)).a != 0:
                    return False
        return True

    def __getitem__(self, key: int):
        """Return currente frame image"""
        cord = self._tiles_cords[key]
        return self._img.subsurface(
            cord[0] * self._frame_widht,
            cord[1] * self._frame_height,
            self._frame_widht,
            self._frame_height,
        )
