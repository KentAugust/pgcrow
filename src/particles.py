"""Particles module"""

import pygame

from .animations import SpriteAnimation
from .maths import Vec2
from .timers import Chronometer


class Particle:
    """Particle base class for simple particles"""

    def __init__(
        self,
        surf: pygame.Surface,
        pos: tuple[int, int],
        vel: tuple[float, float],
        duration: float,
    ) -> None:
        self.image = surf
        self.pos = Vec2(pos)
        self.velocity = Vec2(vel)
        self.duration = duration
        self._chronometer = Chronometer()

    def update(self, delta: float) -> bool:
        """Update position and return False when finished"""
        self._chronometer.update(delta)
        self.pos += self.velocity * delta
        return self.duration - self._chronometer.current_time >= 0.0


class AnimatedParticle(Particle):
    """Particle class that uses SpriteAnimation class"""

    def __init__(
        self, animation: SpriteAnimation, pos: tuple[int, int], vel: tuple[float, float]
    ) -> None:
        self.animation = animation.copy()
        super().__init__(self.animation.image, pos, vel, 0)

    def update(self, delta: float):
        """Update position and return False when finished"""
        self.animation.play(delta)
        self.pos += self.velocity * delta
        return not self.animation.ended

    @property
    def image(self) -> pygame.Surface:
        """ "Get the current frame surface"""
        return self.animation.image


class RectParticle(Particle):
    """Particle class for simple rectangles"""

    cached_images = {}

    def __init__(
        self,
        pos: tuple[int, int],
        vel: tuple[float, float],
        size: tuple[int, int],
        color: [int, int, int],
        duration: float,
    ) -> None:
        self.size = size
        self.color = color
        self._init_image()
        super().__init__(self.image, pos, vel, duration)

    def _init_image(self):
        """Initialize image attribute"""
        cached_lookup = (self.size, self.color)
        if not (cached_image := self.cached_images.get(cached_lookup, None)):
            cached_image = pygame.Surface((self.size, self.size))
            cached_image.fill(self.color)
            self.cached_images[cached_lookup] = cached_image
        self.image = cached_image


class ParticleManager:
    """Class to handle particles"""

    def __init__(self, limit: int | None = None) -> None:
        self._particles: list[Particle] = []
        self.limit = limit

    def update(self, delta: float):
        """Update particle list and each one of them"""
        self._particles = [
            particle for particle in self._particles if particle.update(delta)
        ]

    def add(self, particles: list[Particle]):
        """Add new particles instances"""
        if self.limit and (lenght := len(self._particles)) <= self.limit:
            if lenght == self.limit:
                return
            available = self.limit - lenght
            self._particles.extend(particles[0:available])
            return
        self._particles.extend(particles)

    @property
    def particles(self) -> list[Particle]:
        """Get particles list"""
        return self._particles

    def __len__(self) -> int:
        """Return number of particles"""
        return len(self._particles)
