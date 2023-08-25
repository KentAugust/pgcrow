"""This example uses WindowDisplay instead of WindowScreen
It uses display_size and scale_factor in the config object
"""

import pygame

import pgcrow


class MyGame(pgcrow.game.Game):
    def __init__(self) -> None:

        # you can use both display_size and scale_factor but I recomend you one
        window_config = pgcrow.config.WindowConfig(
            window_size=(640, 360),
            # display_size=(320, 180),
            scale_factor=3,
            title="Example WindowDisplay",
            target_fps=60,
            avalible_window_sizes=[(320, 180), (640, 360), (960, 540), (1280, 720)] # set extra screen sizes we want
        )

        self.window = pgcrow.window.WindowDisplay(window_config) # WindowDisplay blits on a surface
        super().__init__(self.window)

        # stablishing all our scenes
        self.scenes = {
            "main_menu": pgcrow.config.CallableScene(MyMainmenu, {"game": self}),
            "level": pgcrow.config.CallableScene(MyLevel, {"game": self}),
        }
        self.change_scene("main_menu") # initial scene


class MyMainmenu(pgcrow.scene_2d.Scene2D):
    def __init__(self, game: pgcrow.game.Game) -> None:
        super().__init__(game)

        # this will look horrible
        self.font = pygame.font.SysFont('serif', 10) # small fontsize since we are scaling the display

    
    def update(self, dt: float): # Game will pass dt

        # The scene will change if we press 'n' key
        if self.game.keyboard.pressed_this_frame(pygame.K_n):
            self.game.change_scene("level")

        # changing the screen size
        if self.game.keyboard.pressed_this_frame(pygame.K_1):
            self.game.window.update_win_size(1)
        if self.game.keyboard.pressed_this_frame(pygame.K_2):
            self.game.window.update_win_size(2)
        if self.game.keyboard.pressed_this_frame(pygame.K_3):
            self.game.window.update_win_size(3)
        if self.game.keyboard.pressed_this_frame(pygame.K_4):
            self.game.window.update_win_size(4)
        if self.game.keyboard.pressed_this_frame(pygame.K_F11):
            self.game.window.toggle_fullscreen()

    def render(self):

        # player controll
        self.movement = [
            self.game.keyboard.is_held(pygame.K_a), # left
            self.game.keyboard.is_held(pygame.K_d), # right
            self.game.keyboard.is_held(pygame.K_w), # up
            self.game.keyboard.is_held(pygame.K_s), # down
        ]

        txt_surf = self.font.render("Main Menu: press 1-4 to change screen size, f11 to fullscreen", False, (200, 200, 200))
        self.game.window.display.blit(txt_surf, (10, 10))

        mouse_pos = self.game.mouse.get_pos()
        txt_surf = self.font.render(f"Mouse pos {mouse_pos}", False, (200, 200, 200))
        self.game.window.display.blit(txt_surf, (10, 40))

        # important mouse_pos_scaled is a tuple of floats
        mouse_pos_scaled = self.game.mouse.get_pos_scaled(self.game.window.current_win_size, self.game.window.display.get_size())
        txt_surf = self.font.render(f"Mouse pos scaled {mouse_pos_scaled}", False, (200, 200, 200))
        self.game.window.display.blit(txt_surf, (10, 60))


class MyLevel(pgcrow.scene_2d.Scene2D):
    def __init__(self, game: pgcrow.game.Game) -> None:
        super().__init__(game)

        # creating our box player (same as the window_screen example)
        self.box = pygame.Surface((16, 16))
        self.box.fill((38, 250, 218)) # cyan
        self.box_rect = self.box.get_frect()
        self.speed = 120
        self.movement = [False, False, False, False]

    def update(self, dt): # Game will pass dt

        # now we cannot change the screen size sice is a different scene
        # but stiil can toggle fullscreen
        if self.game.keyboard.pressed_this_frame(pygame.K_F11):
            self.game.window.toggle_fullscreen()

        # player controll
        self.movement = [
            self.game.keyboard.is_held(pygame.K_a), # left
            self.game.keyboard.is_held(pygame.K_d), # right
            self.game.keyboard.is_held(pygame.K_w), # up
            self.game.keyboard.is_held(pygame.K_s), # down
        ]

        # updating the player
        movement = (self.movement[1] - self.movement[0], self.movement[3] - self.movement[2])
        self.box_rect.x += movement[0] * self.speed * dt
        self.box_rect.y += movement[1] * self.speed * dt

    def render(self):
        self.game.window.display.blit(self.box, self.box_rect) # rendering the player


if __name__ == "__main__":
    game = MyGame() # Our custom game
    game.run()
