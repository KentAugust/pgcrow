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

        self._actual_scene = None
        self._actual_scene_name = None
        self._run_exit = False
        self._run_enter = False
        self.add_scene(initial_name, initial)
        self.change_scene(initial_name)

    def update(self, dt):
        """Update current scene"""

        self._actual_scene.update(dt)
        self._update_transtion(dt)

    def render(self, display):
        """Render current scene"""

        self._actual_scene.render(display)
        self._render_transtion(display)

    def _update_transtion(self, dt):
        """Update the current scene transition"""

        if self._run_exit:
            if self._actual_scene.on_exit_update(dt):
                self._init_scene()
        if self._run_enter:
            if self._actual_scene.on_enter_update(dt):
                self._run_enter = False

    def _render_transtion(self, display):
        """Update the current scene transition"""

        if self._run_exit:
            self._actual_scene.on_exit_render(display)
        if self._run_enter:
            self._actual_scene.on_enter_render(display)

    def add_scene(self, name: str, scene: CallableScene):
        """Adds new scene to scenes"""

        self._scenes[name] = scene

    def remove_scene(self, name: str):
        """Removes scene from scenes"""

        if name in self._scenes:
            del self._scenes[name]

    def change_scene(self, name: str):
        """Method to change scenes if name is avalible in scenes"""

        if name in self._scenes and not (self._run_enter or self._run_exit):
            self._next_scene = name
            if not self._actual_scene:
                self._init_scene()
            else:
                self._run_exit = True

    def _init_scene(self):
        self._actual_scene: Scene2D = self._scenes[self._next_scene].scene_class(
            **self._scenes[self._next_scene].kwargs
        )
        self._run_enter = True
        self._run_exit = False
        self._actual_scene.set_scene_manager(self)
        self._actual_scene_name = self._next_scene

    def scenes_names(self) -> set:
        "Get all scenes names"

        return set(self._scenes.keys())

    @property
    def actual_scene(self) -> Scene2D:
        """Get a Scene2D object"""
        return self._actual_scene

    @property
    def actual_scene_name(self) -> str:
        """Get the name of the actual scene"""
        return self._actual_scene_name
