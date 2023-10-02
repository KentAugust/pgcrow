import pygame
import src


class WindowContex:
    def __init__(self, window: src.config.Window, window_config: src.config.WindowConfig) -> None:
        self.object = window(window_config)

    def __enter__(self) -> src.config.Window:
        return self.object

    def __exit__(self, type, value, traceback):
        if pygame.display.get_init():
            pygame.quit()
