"""Exmaple for creating a Game, Window, SceneManager objects

Keyboard controlls:
- You can change the size of the window with 1-4 keys
- Toggle fullscreen with F11
- Move the player box with wasd

If run directly with python you can use -_window or -w flag
change the window between screen or display.

ie. python -m pgcrow.examples.game_window -w display

Default: screen
"""

import pygame

import pgcrow


# setting our window configuration
window_config = pgcrow.config.WindowConfig(
    window_size=(640, 360),
    scale_factor=3,
    # set extra screen sizes we want
    avalible_window_sizes=[(320, 180), (640, 360), (960, 540), (1280, 720)],
    can_fullscreen=True, 
    can_resize=True
)

# setting our game configuration
game_config = pgcrow.config.GameConfig(
    title="Example Window",
    target_fps=60,
    clean_color=(30, 30, 30),
    start_fullscreen=False
)

class MyGame(pgcrow.Game):
    def __init__(self, window_type = None) -> None:
        if window_type == "display":
            window = pgcrow.WindowDisplay(window_config) # WindowDisplay blits on a surface
        else:
            window = pgcrow.WindowScreen(window_config) # WindowScreen blits on the screen

        super().__init__(game_config, window)

        # setting scene manager with SceneOne as our initial scene
        self.scene_manager = pgcrow.SceneManager(
            self,
            "My Scene",
            pgcrow.config.CallableScene(MyScene, {"game": self})
        )


class MyScene(pgcrow.Scene2D):
    def __init__(self, game: pgcrow.Game) -> None:
        super().__init__(game)
        self.font = pygame.font.SysFont('lucidaconsole', size=16)

        # creating our box player (same as the window_screen example)
        self.box = pygame.Surface((16, 16))
        self.box.fill((38, 250, 218)) # cyan
        self.box_rect = self.box.get_frect()
        self.speed = 120
        self.movement = [False, False, False, False]

    def update(self, dt): # Game will pass dt
        # changing the screen size
        if self.game.keyboard.just_pressed(pygame.K_1):
            self.game.update_win_size(1)
        if self.game.keyboard.just_pressed(pygame.K_2):
            self.game.update_win_size(2)
        if self.game.keyboard.just_pressed(pygame.K_3):
            self.game.update_win_size(3)
        if self.game.keyboard.just_pressed(pygame.K_4):
            self.game.update_win_size(4)
        if self.game.keyboard.just_pressed(pygame.K_F11):
            self.game.window.toggle_fullscreen()

        # player controll
        self.movement = [
            self.game.keyboard.is_pressed(pygame.K_a), # left
            self.game.keyboard.is_pressed(pygame.K_d), # right
            self.game.keyboard.is_pressed(pygame.K_w), # up
            self.game.keyboard.is_pressed(pygame.K_s), # down
        ]

        # updating the player
        movement = (self.movement[1] - self.movement[0], self.movement[3] - self.movement[2])
        self.box_rect.x += movement[0] * self.speed * dt
        self.box_rect.y += movement[1] * self.speed * dt

    def render(self, display):
        # rendering the player
        display.blit(self.box, self.box_rect)
    
    def render_screen(self, screen):
        # rendering text
        txt_surf = self.font.render("press 1-4 to change screen size, f11 to fullscreen", False, (200, 200, 200))
        screen.blit(txt_surf, (10, 10))

        mouse_pos = self.game.mouse.get_pos()
        txt_surf = self.font.render(f"Mouse pos {mouse_pos}", False, (200, 200, 200))
        screen.blit(txt_surf, (10, 30))

        # important mouse_pos_scaled is a tuple of floats
        mouse_pos_scaled = self.game.mouse.get_pos_scaled(screen.get_size(), self.game.window.display.get_size())
        txt_surf = self.font.render(f"Mouse pos scaled {mouse_pos_scaled}", False, (200, 200, 200))
        screen.blit(txt_surf, (10, 50))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Example for Game, Window and SceneManger objects')
    parser.add_argument('-w', '--window', help='Select type of window (screen or display)')

    args = parser.parse_args()
    window_type = args.window
    
    game = MyGame(window_type) # Our custom game
    game.run()
