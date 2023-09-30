import unittest
import src

from src.config import (
    WindowConfig, GameConfig, Game, CallableScene, Scene2D
    )

wc = WindowConfig(
    window_size=(720, 480),
    scale_factor=2,
    scale_funtion="nearest",
)
gc = GameConfig(
    title="Game Test",
    target_fps=60,
    clean_color=(20, 20, 170)
)


class TestConfigClasses(unittest.TestCase):
    def test_windowconfig_construction(self):
        self.assertEqual((720, 480), wc.window_size)
        self.assertEqual(2, wc.scale_factor)
        self.assertEqual(src.consts.ScaleFuntions.NEAREST, wc.scale_funtion)
        self.assertEqual(None, wc.avalible_window_sizes)
        self.assertEqual(0, wc.depth)
        self.assertEqual(0, wc.vsync)
        self.assertEqual(True, wc.can_fullscreen)
        self.assertEqual(True, wc.can_resize)

    def test_gameconfig_construction(self):
        self.assertEqual("Game Test", gc.title)
        self.assertEqual(60, gc.target_fps)
        self.assertEqual(False, gc.start_fullscreen)
        self.assertEqual((20, 20, 170), gc.clean_color)

    def test_callablescene_construction(self):
        cs = CallableScene(Scene2D, {"game": Game})
        self.assertIn("game", cs.kwargs)
        self.assertEqual(Scene2D, cs.scene_class)
        self.assertEqual(Game, cs.kwargs["game"])
