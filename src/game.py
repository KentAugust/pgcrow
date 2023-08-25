"""## Game"""

from .config import Window
from .event_handler import EventHandler
from .inputs import Keyboard, Mouse
from .scene_manager import SceneManager
from .timers import Deltatimer


class Game:
    """General class that represent the game"""

    def __init__(
        self,
        window: Window,
    ) -> None:
        self.window = window
        self.event_handler = EventHandler()
        self.scene_manager = SceneManager(self)  # set main as an empty scene
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.deltatimer = Deltatimer()

    def run(self):
        """Run the main game loop"""

        while True:
            dt = self.deltatimer.get_dt()
            self.window.clean(self.window.config.clean_color)
            self.event_handler.loop(self.window, self.keyboard, self.mouse)
            self.scene_manager.update(dt)
            self.scene_manager.actual_scene.render()
            self.window.render()
