import unittest
import pygame

from src import WindowScreen, WindowDisplay, WindowScreenGL, WindowDisplayGL
from src.config import WindowConfig

from .test_utils import WindowContex


wc = WindowConfig(
    window_size=(720, 480),
    scale_factor=2,
    scale_funtion="nearest",
)


class TestWindowScreenType(unittest.TestCase):
    def test_construction(self):
        with WindowContex(WindowScreen, wc) as w:
            self.assertEqual(wc, w.config)
            self.assertFalse(pygame.get_init())
            self.assertIsNone(w.screen)

    def test_init_screen(self):
        with WindowContex(WindowScreen, wc) as w:
            w.init_screen()
            ds = pygame.display.get_desktop_sizes()
            self.assertTrue(pygame.get_init())
            self.assertEqual(pygame.Surface, type(w.screen))
            self.assertEqual(pygame.Surface, type(w.display))
            self.assertEqual(ds[0], w.desktop_sizes[0])

    def test_change_size(self):
        with WindowContex(WindowScreen, wc) as w:
            w.init_screen()
            has_changed = w.change_size((640, 320))
            self.assertTrue(has_changed)
            self.assertFalse(w.is_fullscreen)
            self.assertEqual((640, 320), w.current_size)

    def test_toggle_fullscreen(self):
        with WindowContex(WindowScreen, wc) as w:
            w.init_screen()
            self.assertFalse(w.is_fullscreen)
            has_changed = w.toggle_fullscreen()
            self.assertTrue(has_changed)
            self.assertTrue(w.is_fullscreen)
            has_changed = w.toggle_fullscreen()
            self.assertTrue(has_changed)
            self.assertFalse(w.is_fullscreen)

    def test_get_update_function(self):
        with WindowContex(WindowScreen, wc) as w:
            w.init_screen()
            self.assertEqual(pygame.display.update, w.get_update_function())


class TestWindowDisplayType(unittest.TestCase):
    def test_construction(self):
        with WindowContex(WindowDisplay, wc) as w:
            self.assertEqual(wc, w.config)
            self.assertFalse(pygame.get_init())
            self.assertIsNone(w.screen)

    def test_init_screen(self):
        with WindowContex(WindowDisplay, wc) as w:
            w.init_screen()
            ds = pygame.display.get_desktop_sizes()
            self.assertTrue(pygame.get_init())
            self.assertEqual(pygame.Surface, type(w.screen))
            self.assertEqual(pygame.Surface, type(w.display))
            self.assertEqual(ds[0], w.desktop_sizes[0])

    def test_change_size(self):
        with WindowContex(WindowDisplay, wc) as w:
            w.init_screen()
            has_changed = w.change_size((640, 320))
            self.assertTrue(has_changed)
            self.assertFalse(w.is_fullscreen)
            self.assertEqual((640, 320), w.current_size)

    def test_toggle_fullscreen(self):
        with WindowContex(WindowDisplay, wc) as w:
            w.init_screen()
            self.assertFalse(w.is_fullscreen)
            has_changed = w.toggle_fullscreen()
            self.assertTrue(has_changed)
            self.assertTrue(w.is_fullscreen)
            has_changed = w.toggle_fullscreen()
            self.assertTrue(has_changed)
            self.assertFalse(w.is_fullscreen)

    def test_get_update_function(self):
        with WindowContex(WindowDisplay, wc) as w:
            w.init_screen()
            self.assertEqual(pygame.display.update, w.get_update_function())


class TestWindowScreenGLType(unittest.TestCase):
    def test_construction(self):
        with WindowContex(WindowScreenGL, wc) as w:
            self.assertEqual(wc, w.config)
            self.assertFalse(pygame.get_init())
            self.assertIsNone(w.screen)

    def test_init_screen(self):
        with WindowContex(WindowScreenGL, wc) as w:
            w.init_screen()
            ds = pygame.display.get_desktop_sizes()
            self.assertTrue(pygame.get_init())
            self.assertEqual(pygame.Surface, type(w.screen))
            self.assertEqual(pygame.Surface, type(w.display))
            self.assertEqual(ds[0], w.desktop_sizes[0])

    def test_change_size(self):
        with WindowContex(WindowScreenGL, wc) as w:
            w.init_screen()
            has_changed = w.change_size((640, 320))
            self.assertTrue(has_changed)
            self.assertFalse(w.is_fullscreen)
            self.assertEqual((640, 320), w.current_size)

    def test_toggle_fullscreen(self):
        with WindowContex(WindowScreenGL, wc) as w:
            w.init_screen()
            self.assertFalse(w.is_fullscreen)
            has_changed = w.toggle_fullscreen()
            self.assertTrue(has_changed)
            self.assertTrue(w.is_fullscreen)
            has_changed = w.toggle_fullscreen()
            self.assertTrue(has_changed)
            self.assertFalse(w.is_fullscreen)

    def test_get_update_function(self):
        with WindowContex(WindowScreenGL, wc) as w:
            w.init_screen()
            self.assertEqual(None, w.get_update_function())


class TestWindowDisplayGLType(unittest.TestCase):
    def test_construction(self):
        with WindowContex(WindowDisplayGL, wc) as w:
            self.assertEqual(wc, w.config)
            self.assertFalse(pygame.get_init())
            self.assertIsNone(w.screen)

    def test_init_screen(self):
        with WindowContex(WindowDisplayGL, wc) as w:
            w.init_screen()
            ds = pygame.display.get_desktop_sizes()
            self.assertTrue(pygame.get_init())
            self.assertEqual(pygame.Surface, type(w.screen))
            self.assertEqual(pygame.Surface, type(w.display))
            self.assertEqual(ds[0], w.desktop_sizes[0])

    def test_change_size(self):
        with WindowContex(WindowDisplayGL, wc) as w:
            w.init_screen()
            has_changed = w.change_size((640, 320))
            self.assertTrue(has_changed)
            self.assertFalse(w.is_fullscreen)
            self.assertEqual((640, 320), w.current_size)

    def test_toggle_fullscreen(self):
        with WindowContex(WindowDisplayGL, wc) as w:
            w.init_screen()
            self.assertFalse(w.is_fullscreen)
            has_changed = w.toggle_fullscreen()
            self.assertTrue(has_changed)
            self.assertTrue(w.is_fullscreen)
            has_changed = w.toggle_fullscreen()
            self.assertTrue(has_changed)
            self.assertFalse(w.is_fullscreen)

    def test_get_update_function(self):
        with WindowContex(WindowDisplayGL, wc) as w:
            w.init_screen()
            self.assertEqual(None, w.get_update_function())
