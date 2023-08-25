"""## Timers"""

import time


class Timer:
    """Basic timer"""

    def __init__(self) -> None:
        self.__time = time.time()

    @property
    def seconds(self) -> float:
        """Get time in seconds"""

        self.__time = time.time()
        return self.__time % 60

    @property
    def minutes(self) -> float:
        """Get time in minutes"""

        self.__time = time.time()
        return (self.__time % 3600) // 60

    @property
    def hours(self) -> float:
        """Get time in hours"""

        self.__time = time.time()
        return self.__time // 3600


class Deltatimer:
    """Timer for deltatime"""

    def __init__(self) -> None:
        self.__dt = 0
        self.__prev_time = time.time()

    def get_dt(self) -> float:
        """Get deltatime in seconds"""

        self.__dt = time.time() - self.__prev_time
        self.__prev_time = time.time()
        return self.__dt

    @property
    def dt(self) -> float:
        """Returns deltatime"""
        return self.__dt


class Chronometer:
    """chronometer for counting"""

    def __init__(self) -> None:
        self.__current_time = 0
        self.__start_time = 0

    def update(self, dt: float) -> float:
        """Update the currente time"""

        self.__start_time += dt
        self.__current_time = self.__start_time * 1000
        return self.__current_time

    def reset(self):
        """Set current time to 0"""

        self.__start_time = 0
        self.__current_time = 0

    @property
    def current_time(self) -> float:
        """Get currente time"""
        return self.__current_time
