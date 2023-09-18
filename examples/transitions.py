import pygame

import pgcrow


class SceneOne(pgcrow.Scene2D):
    def __init__(self, game: pgcrow.Game) -> None:
        super().__init__(game)
        self.font = pygame.font.SysFont('lucidaconsole', size=16)
        self.timer = pgcrow.timers.Chronometer()

    def on_enter_update(self, dt):
        self.timer.update(dt)

        # change the clean_color
        self.game.config.clean_color = (
            min(round(self.timer.current_time * 10) * 16, 180 ),
            min(round(self.timer.current_time * 10) * 2, 130 ),
            min(round(self.timer.current_time * 10) * 4, 130 )
        )

        if self.timer.current_time >= 1.2:
            # reset the timer because we want to reuse it
            # in the on_exit transition
            self.timer.reset()
            return True # transition finished
        return False

    def on_exit_update(self, dt):
        self.timer.update(dt)

        # change the clean_color
        self.game.config.clean_color = (
            max(10, 180 - round(self.timer.current_time * 10) * 2 ),
            max(10, 130 - round(self.timer.current_time * 10) * 8 ),
            max(10, 130 - round(self.timer.current_time * 10) * 32 )
        )

        if self.timer.current_time >= 1.2:
            return True # transition finished
        return False

    def update(self, dt: float):
        # changing to Scene 2
        # It won't work until the transitions are finished
        if self.game.keyboard.just_pressed(pygame.K_n):
            self.scene_manager.change_scene("Scene 2")

    def render_screen(self, screen: pygame.Surface):
        # blit text
        fps_surf = self.font.render(f"Scene 1: {self.game.clock.get_fps():.0f} fps", False, (220, 220, 220))
        screen.blit(fps_surf, (5, 5))


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

        self.font = pygame.font.SysFont('lucidaconsole', size=16)
        self.timer = pgcrow.timers.Chronometer()

    def on_enter_update(self, dt):
        self.timer.update(dt)

        # drawing a white circle
        pygame.draw.circle(
            self.surf,
            (255, 255, 255),
            (self.surf.get_width()//2, self.surf.get_height()//2),
            round(self.timer.current_time * (self.surf.get_width()/1.6))
        )

        if self.timer.current_time >= 1.2:
            # reset the timer because we want to reuse it
            # in the on_exit transition
            self.timer.reset()
            return True # transition finished
        return False

    def on_exit_update(self, dt):
        self.timer.update(dt)

        self.surf.fill((0, 0, 0))

        # drawing a white circle
        pygame.draw.circle(
            self.surf,
            (255, 255, 255),
            (self.surf.get_width()//2, self.surf.get_height()//2),
            self.surf.get_height() - round(self.timer.current_time * (self.surf.get_width()/1.6))
        )
        self.surf.set_colorkey((255, 255, 255))

        if self.timer.current_time >= 1.2:
            self.game.config.clean_color = (0, 0, 0)
            return True # transition finished
        return False

    def update(self, dt: float):
        # transition to Scene 1
        # It won't work until the transitions are finished
        if self.game.keyboard.just_pressed(pygame.K_n):
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

    def render(self, display: pygame.Surface):
        # blit player
        display.blit(self.player, self.pos)

    def render_screen(self, screen: pygame.Surface):
        # blit text
        fps_surf = self.font.render(f"Scene 2: {self.game.clock.get_fps():.0f} fps", False, (220, 220, 220))
        screen.blit(fps_surf, (5, 5))

    def on_enter_render(self, display: pygame.Surface):
        # blit transition surface
        display.blit(self.surf, (0, 0))

    def on_exit_render(self, display: pygame.Surface):
        # blit transition surface
        display.blit(self.surf, (0, 0))


class MyGame(pgcrow.Game):
    def __init__(self) -> None:
        # setting our window configuration
        win_config = pgcrow.config.WindowConfig(
            window_size=(720, 480),
            scale_factor=2
        )

        # setting our game configuration
        game_config = pgcrow.config.GameConfig(
            title="Example Transitions", 
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
