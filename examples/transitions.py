import pygame

import pgcrow


class SceneOne(pgcrow.Scene2D):
    def __init__(self, game: pgcrow.Game) -> None:
        super().__init__(game)
        self.font = pygame.font.SysFont('lucidaconsole', size=8)
        self.timer = pgcrow.timers.Chronometer()

    def on_enter(self, dt):
        self.timer.update(dt)

        # change the clean_color
        self.game.config.clean_color = (
            min(round(self.timer.current_time/100) * 16, 180 ),
            min(round(self.timer.current_time/100) * 2, 130 ),
            min(round(self.timer.current_time/100) * 4, 130 )
        )

        if self.timer.current_time >= 1200:
            # reset the timer because we want to reuse it
            # in the on_exit transition
            self.timer.reset()
            return True # transition finished
        return False

    def on_exit(self, dt):
        self.timer.update(dt)

        # change the clean_color
        self.game.config.clean_color = (
            max(10, 180 - round(self.timer.current_time/100) * 2 ),
            max(10, 130 - round(self.timer.current_time/100) * 8 ),
            max(10, 130 - round(self.timer.current_time/100) * 32 )
        )

        if self.timer.current_time >= 1200:
            return True # transition finished
        return False

    def update(self, dt: float):
        # changing to Scene 2
        if self.game.keyboard.pressed_this_frame(pygame.K_n):
            self.scene_manager.change_scene("Scene 2")

    def render(self):
        # blit text
        fps_surf = self.font.render(f"Scene 1", False, (220, 220, 220))
        self.game.window.display.blit(fps_surf, (5, 5))


class SceneTwo(pgcrow.Scene2D):
    def __init__(self, game: pgcrow.Game) -> None:
        super().__init__(game)
        self.game.config.clean_color = (20, 200, 60)

        # creating a surface for the on_enter transition
        self.surf = pygame.Surface(self.game.window.display.get_size())
        self.surf.set_colorkey((255, 255, 255))

        # player stuff
        self.player = pygame.Surface((16, 16))
        self.player.fill((20, 100, 220))
        self.pos = pgcrow.maths.Vec2(146, 76) # arbitrary position
        self.vec = pgcrow.maths.Vec2()
        self.speed = 180
        self.movement = [False, False, False, False]

        self.font = pygame.font.SysFont('lucidaconsole', size=8)
        self.timer = pgcrow.timers.Chronometer()

    def on_enter(self, dt):
        self.timer.update(dt)

        # drawing a white circle
        pygame.draw.circle(
            self.surf,
            (255, 255, 255),
            (self.surf.get_width()//2, self.surf.get_height()//2),
            round(self.timer.current_time * (self.surf.get_width()/1600))
        )

        if self.timer.current_time >= 1200:
            # reset the timer because we want to reuse it
            # in the on_exit transition
            self.timer.reset()
            return True # transition finished
        return False

    def on_exit(self, dt):
        self.timer.update(dt)

        # this is expencive since we are creating new surface every frame
        self.surf = pygame.Surface(self.game.window.display.get_size())
        # drawing a white circle
        pygame.draw.circle(
            self.surf,
            (255, 255, 255),
            (self.surf.get_width()//2, self.surf.get_height()//2),
            self.surf.get_height() - round(self.timer.current_time * (self.surf.get_width()/1200))
        )
        self.surf.set_colorkey((255, 255, 255))

        if self.timer.current_time >= 1200:
            return True # transition finished
        return False

    def update(self, dt: float):
        # transition to Scene 1
        if self.game.keyboard.pressed_this_frame(pygame.K_n):
            self.scene_manager.change_scene("Scene 1")

        # controll player
        self.movement = [
            self.game.keyboard.is_held(pygame.K_a), # left
            self.game.keyboard.is_held(pygame.K_d), # right
            self.game.keyboard.is_held(pygame.K_w), # up
            self.game.keyboard.is_held(pygame.K_s), # down
        ]

        # update player pos
        move = [self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]]
        self.vec.x = move[0] * self.speed * dt
        self.pos.x += self.vec.x
        self.vec.y = move[1] * self.speed * dt
        self.pos.y += self.vec.y

    def render(self):
        # blit player
        self.game.window.display.blit(self.player, self.pos)

        # blit text
        fps_surf = self.font.render(f"Scene 2: {self.game.clock.get_fps():.0f} fps", False, (220, 220, 220))
        self.game.window.display.blit(fps_surf, (5, 5))

        # blit transition surface
        self.game.window.display.blit(self.surf, (0, 0))


class MyGame(pgcrow.Game):
    def __init__(self) -> None:
        # setting our window configuration
        win_config = pgcrow.config.WindowConfig(
            window_size=(720, 480),
            scale_factor=2,
            avalible_window_sizes=[(1280, 720), (640, 360), (320, 180)],
        )

        # setting our game configuration
        game_config = pgcrow.config.GameConfig(
            title="pgcrow testing", 
            target_fps=60,
        )
        super().__init__(game_config, pgcrow.WindowDisplay(win_config))

        # setting scene manager with SceneOne as our initial scene
        self.scene_manager = pgcrow.SceneManager(
            self,
            "Scene 1",
            pgcrow.config.CallableScene(SceneOne, {"game": self})
            )
        
        # adding a new scene
        self.scene_manager.add_scene("Scene 2", pgcrow.config.CallableScene(SceneTwo, {"game": self}))


if __name__ == "__main__":
    MyGame().run()
