"""Scene Manager"""

from .config import CallableScene, Game
from .scene_2d import Scene2D


class SceneManager:
    """Class for hanglind scenes"""

    def __init__(
        self,
        game: Game,
        initial_name: str = "main",
        initial: CallableScene | None = None,
    ):
        self.game = game
        self._scenes = {}

        if initial is None:
            initial = CallableScene(Scene2D, {"game": game})

        self.add_scene(initial_name, initial)
        self.change_scene(initial_name)

    def add_scene(self, name: str, scene: CallableScene):
        """Adds new scene to scenes"""

        self._scenes[name] = scene

    def remove_scene(self, name: str):
        """Removes scene from scenes"""

        if name in self._scenes:
            del self._scenes[name]

    def change_scene(self, name: str):
        """Method to change scenes if name is avalible in scenes"""

        if name in self._scenes:
            self._actual_scene: Scene2D = self._scenes[name].scene_class(
                **self._scenes[name].kwargs
            )
            self._actual_scene.set_scene_manager(self)
            self._actual_scene_name = name

    def scenes_names(self) -> set:
        "Get all scenes names"

        return set(self._scenes.keys())

    @property
    def actual_scene(self) -> Scene2D:
        return self._actual_scene

    @property
    def actual_scene_name(self) -> str:
        return self._actual_scene_name
