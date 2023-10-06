"""Input protocol"""

from typing import Annotated, Any, Optional, Protocol

from pygame.event import Event

InputKey = Annotated[int, str]


class Input(Protocol):
    """Class that represent a general input type"""

    def handle_event(self, event: Event):
        """Handle a single event"""

    def get_input_data(self, key: InputKey) -> Optional[Any]:
        """Get data of an specific input"""

    def is_pressed(self, key: InputKey) -> bool:
        """Check if input key is pressed"""

    def just_pressed(self, key: InputKey) -> bool:
        """Check if input key is pressed in this exact frame"""

    def just_released(self, key: InputKey) -> bool:
        """Check if input key stop being pressed in this exact frame"""

    def press_time(self, key: InputKey) -> Optional[float]:
        """Get the time that an input key was pressed"""

    def press_frame(self, key: InputKey) -> Optional[int]:
        """Get the frame that an input key was pressed"""

    def hold_time(self, key: InputKey) -> Optional[float]:
        """Return how long an input key is being pressed"""

    def hold_frames(self, key: InputKey) -> Optional[int]:
        """Return how many frames an input key is being pressed"""

    def release_time(self, key: InputKey) -> Optional[float]:
        """Return the time an input key stop being pressed"""

    def release_frame(self, key: InputKey) -> Optional[int]:
        """Return the frame an input key stop being pressed"""

    def time_since_release(self, key: InputKey) -> Optional[float]:
        """Return how long an input key stop pressed"""

    def frames_since_release(self, key: InputKey) -> Optional[int]:
        """Return how many frames an input key stop pressed"""
