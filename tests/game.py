import unittest

import pygame

from src import EventHandler, Game, Scene2D, SceneManager, WindowScreen
from src.config import GameConfig, WindowConfig
from src.inputs import Keyboard, Mouse
from src.maths import Vec2
from src.timers import Delta

from .test_utils import WindowContex

wc = WindowConfig((720, 480), 2, "nearest", [(360, 240)])
gc = GameConfig("TestWindow", 60)


class TestGameType(unittest.TestCase):
    def test_game_contruction(self):
        with WindowContex(WindowScreen, wc) as w:
            g = Game(gc, w)
            self.assertEqual(WindowScreen, type(g.window))
            self.assertEqual(Keyboard, type(g.keyboard))
            self.assertEqual(Mouse, type(g.mouse))
            self.assertEqual(EventHandler, type(g.event_handler))
            self.assertEqual(SceneManager, type(g.scene_manager))
            self.assertEqual(pygame.Clock, type(g.clock))
            self.assertEqual(Delta, type(g.deltatimer))
            self.assertEqual(Vec2, type(g.display_offset))

    def test_init_game(self):
        with WindowContex(WindowScreen, wc) as w:
            g = Game(gc, w)
            g.init_game()
            self.assertTrue(pygame.display.get_init())
            self.assertEqual(Scene2D, type(g.scene_manager.actual_scene))

    def test_set_title(self):
        with WindowContex(WindowScreen, wc) as w:
            g = Game(gc, w)
            g.init_game()
            title = pygame.display.get_caption()
            self.assertEqual("TestWindow", title[0])
            g.set_title("New Title")
            title = pygame.display.get_caption()
            self.assertEqual("New Title", title[0])

    def test_quit(self):
        with WindowContex(WindowScreen, wc) as w:
            g = Game(gc, w)
            g.init_game()
            self.assertTrue(pygame.display.get_init())
            try:
                g.quit()
            except SystemExit:
                self.assertFalse(pygame.display.get_init())

    def test_update_win_size(self):
        with WindowContex(WindowScreen, wc) as w:
            g = Game(gc, w)
            g.init_game()
            self.assertEqual((720, 480), w.current_size)
            self.assertEqual((360, 240), g.update_win_size(2))
            self.assertEqual((360, 240), w.current_size)

    def test_start_fullscreen(self):
        with WindowContex(WindowScreen, wc) as w:
            gcc = GameConfig("TestWindow", 60, True)
            g = Game(gcc, w)
            g.init_game()
            self.assertTrue(w.is_fullscreen)
            self.assertEqual(w.desktop_sizes[0], w.current_size)
