"""Constants"""

from enum import StrEnum


class ScaleFuntions(StrEnum):
    """Enum for scale funtion on WindowConfig"""

    SMOOTH = "smooth"
    NEAREST = "nearest"


class Math:
    """Math related enum"""

    PI = 3.141592653589793
    TAU = 6.283185307179586
    PHI = 1.618033988749895
    E = 2.718281828459045
    G = 9.80665


class JoyGetInputFuction(StrEnum):
    BUTTONS = "buttons"
    AXES = "axes"
