"""## Timers"""

import time


class TimeClock:
    """Basic timer"""

    @staticmethod
    def time() -> float:
        """Get time"""
        return time.time()

    @staticmethod
    def seconds() -> float:
        """Get time in seconds"""
        return time.time() % 60

    @staticmethod
    def minutes() -> float:
        """Get time in minutes"""
        return (time.time() % 3600) // 60

    @staticmethod
    def hours() -> float:
        """Get time in hours"""
        return time.time() // 3600


class Delta:
    """Timer for deltatime"""

    def __init__(self) -> None:
        self._delta = 0
        self._prev_time = time.time()

    def get_delta(self) -> float:
        """Get deltatime in seconds"""
        self._delta = time.time() - self._prev_time
        self._prev_time = time.time()
        return self._delta

    @property
    def deltatime(self) -> float:
        """Returns deltatime"""
        return self._delta


class Chronometer:
    """chronometer for counting"""

    def __init__(self) -> None:
        self._current_time = 0
        self._start_time = 0

    def update(self, delta: float) -> float:
        """Update the currente time"""
        self._start_time += delta
        self._current_time = self._start_time
        return self._current_time

    def reset(self):
        """Set current time to 0"""
        self._start_time = 0
        self._current_time = 0

    @property
    def current_time(self) -> float:
        """Get currente time in seconds"""
        return self._current_time

    @property
    def current_time_ms(self) -> float:
        """Get currente time in miliseconds"""
        return self._current_time * 1000
