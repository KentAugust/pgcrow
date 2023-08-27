"""Math module"""

import math

import pygame


class Vec2(pygame.Vector2):
    """Wrapper for pygame.Vector2"""

    # It desn't add nothing new for now


class Vec3(pygame.Vector3):
    """Wrapper for pygame.Vector3"""

    # It desn't add nothing new for now


def deg_to_rad(angle: float) -> float:
    """Converts angles from degrees to radians"""
    return (angle * math.pi) / 180


def rad_to_deg(angle: float) -> float:
    """Converts angles from radians to degrees"""
    return (angle * 360) / (2 * math.pi)


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
