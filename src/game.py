"""## Game"""

from .event_handler import EventHandler
from .scene_2d import Scene2D
from .inputs import Keyboard, Mouse
from .timers import Deltatimer
from .window import Window
from .config import CallableScene


class Game:
    """General class that represent the game"""

    def __init__(self, window: Window) -> None:
        self.window = window
        self.event_handler = EventHandler()
        self.scenes = {
            "main": CallableScene(Scene2D, {"game": self})  # set main as an empty scene
        }
        self.change_scene("main")  # init empty scene
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.deltatimer = Deltatimer()

    def change_scene(self, name: str):
        """Method to change scenes if name is avalible in scenes"""

        if name in self.scenes:
            self.actual_scene: Scene2D = self.scenes[name].scene_class(
                **self.scenes[name].kwargs
            )

    def run(self):
        """Run the main game loop"""

        while True:
            dt = self.deltatimer.get_dt()
            self.window.clean((0, 0, 0))
            self.event_handler.loop(self.window, self.keyboard, self.mouse)
            self.actual_scene.update(dt)
            self.actual_scene.render()
            self.window.render()
