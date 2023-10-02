"""Scene Manager"""

from typing import Self

import pygame

from .config import CallableScene, Game
from .scene_2d import Scene2D


class SceneManager:  # pylint: disable=R0902
    """Class for hanglind scenes"""

    def __init__(
        self,
        game: Game,
        initial_name: str = "main",
        initial: CallableScene | None = None,
    ):
        self._scenes = {}
        self._actual_scene = None
        self._actual_scene_name = None
        self._previus_scene_name = None
        self._next_scene_name = None
        self._run_exit = False
        self._run_enter = False
        self._initial_name = initial_name
        self.game = game

        if initial is None:
            initial = CallableScene(Scene2D, {"game": game})

        self.add_scene(initial_name, initial)

    def start_initial_scene(self) -> Self:
        """Instantiate the initial scene"""
        if not pygame.get_init():
            raise pygame.error
        self.change_scene(self._initial_name)
        return self

    def update(self, delta: float):
        """Update current scene"""
        self._actual_scene.update(delta)
        self.__update_transition(delta)

    def render(self, display: pygame.Surface):
        """Render current scene"""
        self._actual_scene.render(display)
        self.__render_transition(display)

    def render_screen(self, screen: pygame.Surface):
        """Render current scene onto screen"""
        self._actual_scene.render_screen(screen)

    def __update_transition(self, delta: float):
        """Update the current scene transition"""
        if self._run_exit:
            if self._actual_scene.on_exit_update(delta):
                self.__init_scene()
        if self._run_enter:
            if self._actual_scene.on_enter_update(delta):
                self._run_enter = False

    def __render_transition(self, display: pygame.Surface):
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
            self._next_scene_name = name
            if not self._actual_scene:
                self.__init_scene()
            else:
                self._run_exit = True

    def __init_scene(self):
        """Instantiate the next scene"""
        self._actual_scene: Scene2D = self._scenes[self._next_scene_name].scene_class(
            **self._scenes[self._next_scene_name].kwargs
        )
        self._run_enter = True
        self._run_exit = False
        self._previus_scene_name = self._actual_scene_name
        self._actual_scene.set_scene_manager(self)
        self._actual_scene_name = self._next_scene_name

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
