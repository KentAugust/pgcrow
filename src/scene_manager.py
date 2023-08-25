"""Scene Manager"""

from .scene_2d import Scene2D
from .config import Game, CallableScene


class SceneManager:
    """Class for hanglind scenes"""

    def __init__(
        self,
        game: Game,
        initial_name: str = "main",
        initial: CallableScene | None = None,
    ):
        self.game = game
        self.scenes = {}

        if initial is None:
            initial = CallableScene(Scene2D, {"game": game})

        self.add_scene(initial_name, initial)
        self.change_scene(initial_name)

    def add_scene(self, name: str, scene: CallableScene):
        """Adds new scene to scenes"""

        self.scenes[name] = scene

    def remove_scene(self, name: str):
        """Removes scene from scenes"""

        if name in self.scenes:
            del self.scenes[name]

    def change_scene(self, name: str):
        """Method to change scenes if name is avalible in scenes"""

        if name in self.scenes:
            self.actual_scene: Scene2D = self.scenes[name].scene_class(
                **self.scenes[name].kwargs
            )
            self.actual_scene.set_scene_manager(self)
