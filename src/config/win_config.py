"""Window configuration"""

from dataclasses import dataclass


@dataclass
class WindowConfig:
    """Window configuration class"""

    window_size: tuple[int, int]
    display_size: tuple[int, int] | None = None
    scale_factor: float = 1.0
    avalible_window_sizes: list[tuple[int, int]] | None = None
    title: str = "Pygame Window"
    target_fps: int = 0
    depth: int = 0
    vsync: int = 0
    start_fullscreen: bool = False
    can_fullscreen: bool = True
    can_resize: bool = True
