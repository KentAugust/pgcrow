"""Math module"""

import math

import pygame


class Vec2(pygame.Vector2):
    """Wrapper for pygame.Vector2"""

    def stringify(self, sep: str = ",") -> str:
        """Returns a vector representation with the given separator
        ie. with "," as separator:
        Vec2(4.0, 2.23) -> "4.0,2.23"
        """
        return f"{self.x}{sep}{self.y}"

    @staticmethod
    def unstringify(string: str, sep: str = ",") -> "Vec2":
        """Returns a new Vect2 from a string
        ie. with "," as separator:
        "4.0,2.23" -> Vec2(4.0, 2.23)
        """
        vec_elements = string.split(sep)
        x, y = vec_elements[0], vec_elements[1]
        return Vec2(float(x), float(y))


class Vec3(pygame.Vector3):
    """Wrapper for pygame.Vector3"""

    def stringify(self, sep: str = ",") -> str:
        """Returns a vector representation with the given separator
        ie. with "," as separator:
        Vec3(4.0, 2.23, 0.52) -> "4.0,2.23,0.52"
        """
        return f"{self.x}{sep}{self.y}{sep}{self.z}"

    @staticmethod
    def unstringify(string: str, sep: str = ",") -> "Vec3":
        """Returns a new Vect3 from a string
        ie. with "," as separator:
        "4.0,2.23,0.52" -> Vec3(4.0, 2.23, 0.52)
        """
        vec_elements = string.split(sep)
        x, y, z = vec_elements[0], vec_elements[1], vec_elements[2]
        return Vec3(float(x), float(y), float(z))


def deg_to_rad(angle: float) -> float:
    """Converts angles from degrees to radians"""
    return (angle * math.pi) / 180


def rad_to_deg(angle: float) -> float:
    """Converts angles from radians to degrees"""
    return (angle * 180) / math.pi


def angle_to_direction(angle: float) -> Vec2:
    """Transform an angle in radians to a vector
    (Note that due to pygame's inverted y coordinate system, the rotation will look clockwise
    if displayed).
    """
    return Vec2(math.cos(angle), math.sin(angle))


def direction_to_angle(vec: Vec2) -> float:
    """Transform a vector to an angle in radians
    (Note that due to pygame's inverted y coordinate system, the rotation will look clockwise
    if displayed).
    """
    return math.atan2(vec.y, vec.x)
