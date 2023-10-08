"""## Joystick handling"""

from dataclasses import dataclass
from typing import Any, Optional

import pygame

from ..consts import JoyGetInputFuction
from ..timers import TimeClock
from .general import InputKey


@dataclass
class JoyButton:  # pylint: disable=R0902
    """JoyButton dataclass"""

    joy: int
    instance_id: int
    button: Any
    pressed: bool
    start_time: float
    start_frame: int
    end_time: Optional[float]
    end_frame: Optional[int]


@dataclass
class Axi:  # pylint: disable=R0902
    """JoyAxi dataclass"""

    joy: int
    instance_id: int
    axis: int
    value: float
    moving: bool
    start_time: float
    start_frame: int
    end_time: Optional[float]
    end_frame: Optional[int]
    sensitivity: float = 1.0


class Joystick:  # pylint: disable=R0902 disable=R0904
    """Class for handling keys events"""

    _all_joysticks: dict[str, pygame.joystick.JoystickType] = {}
    _active_joys_id: list[int] = []

    def __init__(self, get_input_funtion_type=JoyGetInputFuction.BUTTONS) -> None:
        joystick = self._connect_joystick()
        self._instance_id = joystick.get_instance_id()
        self._guid = joystick.get_guid()
        self._joystick_active = True
        self._buttons: dict[InputKey, JoyButton] = {}
        self._axis: dict[InputKey, Axi] = {}
        Joystick._all_joysticks[self._guid] = joystick
        Joystick._active_joys_id.append(self._instance_id)
        self.change_get_input_function(get_input_funtion_type)

    def _connect_joystick(self):
        """Search for an avalibe id and return a new joystick"""
        if len(Joystick._active_joys_id) == pygame.joystick.get_count():
            raise pygame.error("There aren't more joystick connected.")

        for i in range(pygame.joystick.get_count()):
            if i not in Joystick._active_joys_id:
                break
        return pygame.Joystick(i)

    def change_get_input_function(self, funtion_type=JoyGetInputFuction.BUTTONS):
        """Change get_input_data function between get_axi and get_button"""
        match funtion_type:
            case JoyGetInputFuction.AXES:
                self.get_input_data = self.get_axi
            case _:
                self.get_input_data = self.get_button

    def handle_event(self, event: pygame.Event) -> None:
        """Handle a single event"""
        match event.type:
            case pygame.JOYDEVICEADDED:
                if event.guid == self._guid and not self._joystick_active:
                    if self._instance_id in Joystick._active_joys_id:
                        # assign a new joystick
                        Joystick._all_joysticks[self._guid] = self._connect_joystick()
                    try:
                        # init joystick if is connected
                        Joystick._all_joysticks[self._guid].init()
                    except pygame.error:
                        # assign a new joystick
                        Joystick._all_joysticks[self._guid] = self._connect_joystick()

                    self._instance_id = Joystick._all_joysticks[
                        self._guid
                    ].get_instance_id()
                    self._joystick_active = True
                    Joystick._active_joys_id.append(self._instance_id)
            case pygame.JOYDEVICEREMOVED:
                if event.instance_id == self._instance_id and self._joystick_active:
                    Joystick._all_joysticks[self._guid].quit()
                    Joystick._active_joys_id.remove(self._instance_id)
                    self._joystick_active = False
                    self._buttons = {}
                    self._axis = {}
            case pygame.JOYAXISMOTION:
                if event.instance_id != self._instance_id:
                    return
                if event.axis not in self._axis:
                    start_time = TimeClock.seconds()
                    start_frame = pygame.time.get_ticks()
                    self._axis[event.axis] = Axi(
                        event.joy,
                        event.instance_id,
                        event.axis,
                        event.value,
                        True,
                        start_time,
                        start_frame,
                        None,
                        None,
                    )
                else:
                    axi = self._axis[event.axis]
                    axi.joy = event.joy
                    axi.instance_id = event.instance_id
                    axi.axis = event.axis

                    prescision = 0 + 1 * axi.sensitivity
                    axi.value = event.value * prescision
                    if prescision * -10e-5 <= axi.value <= prescision * 10e-5:
                        axi.moving = False
                        axi.end_time = TimeClock.seconds()
                        axi.end_frame = pygame.time.get_ticks()
                    else:
                        axi.moving = True
                        axi.end_time = None
                        axi.end_frame = None
            case pygame.JOYBUTTONDOWN:
                if event.instance_id != self._instance_id:
                    return
                start_time = TimeClock().seconds()
                start_frame = pygame.time.get_ticks()
                self._buttons[event.button] = JoyButton(
                    event.joy,
                    event.instance_id,
                    event.button,
                    True,
                    start_time,
                    start_frame,
                    None,
                    None,
                )
            case pygame.JOYBUTTONUP:
                if event.instance_id != self._instance_id:
                    return
                button: JoyButton = self._buttons[event.button]
                button.pressed = False
                button.end_time = TimeClock.seconds()
                button.end_frame = pygame.time.get_ticks()
            # TODO: Handle pygame.JOYBALLMOTION and pygame.JOYHATMOTION events

    # buttons mehtods
    def get_button(self, key: InputKey) -> Optional[JoyButton]:
        """Get data of an specific button"""
        return self._buttons[key] if key in self._buttons else None

    def is_pressed(self, key: InputKey) -> bool:
        """Check if a button is pressed"""
        return k.pressed if (k := self.get_button(key)) else False

    def just_pressed(self, key: InputKey) -> bool:
        """Check if a button is pressed in this exact frame"""
        return self.hold_frames(key) == 0

    def just_released(self, key: InputKey) -> bool:
        """Check if a button stop being pressed in this exact frame"""
        return k.end_frame if (k := self.get_button(key)) else None

    def press_time(self, key: InputKey) -> Optional[float]:
        """Get the time that a button was pressed"""
        return k.start_time if (k := self.get_button(key)) else None

    def press_frame(self, key: InputKey) -> Optional[int]:
        """Get the frame that a button was pressed"""
        return k.start_frame if (k := self.get_button(key)) else None

    def hold_time(self, key: InputKey) -> Optional[float]:
        """Return how long a button is being pressed"""
        return (
            TimeClock.seconds() - k.start_time if (k := self.get_button(key)) else None
        )

    def hold_frames(self, key: InputKey) -> Optional[int]:
        """Return how many frames a button is being pressed"""
        return (
            pygame.time.get_ticks() - k.start_frame
            if (k := self.get_button(key))
            else None
        )

    def release_time(self, key: InputKey) -> Optional[float]:
        """Return the time a button stop being pressed"""
        return k.end_time if (k := self.get_button(key)) else None

    def release_frame(self, key: InputKey) -> Optional[int]:
        """Return the frame a button stop being pressed"""
        return k.end_frame if (k := self.get_button(key)) else None

    def time_since_release(self, key: InputKey) -> Optional[float]:
        """Return how long a button stop pressed"""
        return TimeClock.seconds() - k if (k := self.release_time(key)) else None

    def frames_since_release(self, key: InputKey) -> Optional[int]:
        """Return how many frames a button stop pressed"""
        return pygame.time.get_ticks() - k if (k := self.release_frame(key)) else None

    # axes methods
    def get_axi(self, key: InputKey) -> Optional[Axi]:
        """Get data of an specific axi"""
        return self._axis[key] if key in self._axis else None

    def is_moving(self, key: InputKey) -> bool:
        """Check if an axi is moving"""
        return k.moving if (k := self.get_axi(key)) else False

    def just_move(self, key: InputKey) -> bool:
        """Check if an axi is moving in this exact frame"""
        return self.hold_frames_axi(key) == 0

    def just_released_axi(self, key: InputKey) -> bool:
        """Check if an axi stop moving in this exact frame"""
        return k.end_frame if (k := self.get_axi(key)) else None

    def move_time(self, key: InputKey) -> Optional[float]:
        """Get the time that an axi start moving"""
        return k.start_time if (k := self.get_axi(key)) else None

    def move_frame(self, key: InputKey) -> Optional[int]:
        """Get the frame that an axi start moving"""
        return k.start_frame if (k := self.get_axi(key)) else None

    def hold_time_axi(self, key: InputKey) -> Optional[float]:
        """Return how long an axi is moving"""
        return TimeClock.seconds() - k.start_time if (k := self.get_axi(key)) else None

    def hold_frames_axi(self, key: InputKey) -> Optional[int]:
        """Return how many frames an axi is moving"""
        return (
            pygame.time.get_ticks() - k.start_frame
            if (k := self.get_axi(key))
            else None
        )

    def release_time_axi(self, key: InputKey) -> Optional[float]:
        """Return the time an axi stop moving"""
        return k.end_time if (k := self.get_axi(key)) else None

    def release_frame_axi(self, key: InputKey) -> Optional[int]:
        """Return the frame an axi stop moving"""
        return k.end_frame if (k := self.get_axi(key)) else None

    def time_since_release_axi(self, key: InputKey) -> Optional[float]:
        """Return how long an axi stop moving"""
        return TimeClock.seconds() - k if (k := self.release_time_axi(key)) else None

    def frames_since_release_axi(self, key: InputKey) -> Optional[int]:
        """Return how many frames an axi stop moving"""
        return (
            pygame.time.get_ticks() - k if (k := self.release_frame_axi(key)) else None
        )

    def change_axi_precision(self, key: InputKey, sensitivity: float):
        """Change the sensitivity of an axi"""
        if key in self._axis:
            sensitivity = max(0.0, min(sensitivity, 1.0))
            self._axis[key].sensitivity = sensitivity

    @property
    def joystick_type(self):
        """Get JoystickType"""
        return Joystick._all_joysticks[self._guid]

    @property
    def instance_id(self):
        """Get joystick instance id"""
        return self._instance_id

    @property
    def is_active(self):
        """It's joystick active"""
        return self._joystick_active

    @property
    def joystick_buttons(self):
        """JoystickType.get_button for all buttons"""
        if not self._joystick_active:
            return []
        return [
            Joystick._all_joysticks[self._guid].get_button(i)
            for i in range(Joystick._all_joysticks[self._guid].get_numbuttons())
        ]

    @property
    def joystick_axis(self):
        """JoystickType.get_axis for all axes"""
        if not self._joystick_active:
            return []
        return [
            Joystick._all_joysticks[self._guid].get_axis(i)
            for i in range(Joystick._all_joysticks[self._guid].get_numaxes())
        ]

    @property
    def joystick_balls(self):
        """JoystickType.get_ball for all balls"""
        if not self._joystick_active:
            return []
        return [
            Joystick._all_joysticks[self._guid].get_ball
            for i in range(Joystick._all_joysticks[self._guid].get_numballs())
        ]
