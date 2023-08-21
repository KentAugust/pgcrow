"""Window configuration"""

from dataclasses import dataclass


@dataclass
class WindowConfig:
    """Window configuration class"""

    window_size: tuple[int, int]
    display_size: tuple[int, int] | None = None
    scale_factor: float = 1.0
    target_fps: int = 0
    depth: int = 0
    vsync: int = 0
    can_fullscreen: bool = True
    can_resize: bool = True
