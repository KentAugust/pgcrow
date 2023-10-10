import moderngl
import pgcrow
import pygame

from array import array

window_config = pgcrow.config.WindowConfig((500, 500))
game_config = pgcrow.config.GameConfig("Example WindowScreenGL", 60, clean_color=(51, 77, 77))


class MyGame(pgcrow.Game):
    """This Examples requires moderngl ^5.8.2"""

    def __init__(self) -> None:
        super().__init__(game_config, pgcrow.WindowScreenGL(window_config))
        self.scene_manager = pgcrow.SceneManager(
            self,
            initial=pgcrow.config.CallableScene(Level, {"game": self})
        )


class Level(pgcrow.Scene2D):
    def __init__(self, game: MyGame) -> None:
        super().__init__(game)

        self.ctx = moderngl.create_context()
        vertices = self.ctx.buffer(data=array("f", [
            #   positions       uvs
             0.5,  0.5, 0.0,  1.0, 1.0, # top right
             0.5, -0.5, 0.0,  1.0, 0.0, # bottom right
            -0.5, -0.5, 0.0,  0.0, 0.0, # bottom left
            -0.5,  0.5, 0.0,  0.0, 1.0, # top left
        ]))

        indices = self.ctx.buffer(data=array("I", [
            0, 1, 3,
            1, 2, 3,
        ]))

        vert_shader = """
        #version 330 core

        in vec3 pos;
        in vec2 vertUV;

        out vec2 uv;

        void main() {
            gl_Position = vec4(pos, 1.0);
            uv = vertUV;
        }
        """

        frag_shader = """
        #version 330 core

        const float TAU = 6.28318530718;

        in vec2 uv;
        out vec4 fragColor;

        uniform vec4 colorA = vec4(1.0, 0.2, 0.0, 1.0);
        uniform vec4 colorB = vec4(0.0, 0.0, 1.0, 1.0);
        uniform float time = 0.0;

        float simpleLerp(float a, float b, float t) {
            return (a-a*t)+b*t;
        }

        float inverseLerp(float a, float b, float v) {
            return (v-a)/(b-a);
        }

        vec4 vectorLerp(vec4 a, vec4 b, float t) {
            return vec4(
                simpleLerp(a.x, b.x, t),
                simpleLerp(a.y, b.y, t),
                simpleLerp(a.z, b.z, t),
                simpleLerp(a.w, b.w, t)
            );
        }

        void main() {
            vec2 newUV = vec2(tan(uv.x) - cos(time) * 0.1, tan(uv.y) + sin(time) * 0.4);

            float xOffset = sin(newUV.x * TAU * 8) * 0.01;
            float yOffset = sin(newUV.y * TAU * 8) * 0.01;

            float t = sin((newUV.y + xOffset + time * 0.2) * TAU * 4) * 0.5 + yOffset;
            fragColor = vectorLerp(colorA, colorB, t) * colorA;
        }
        """

        self.program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(vertices, '3f 2f', 'pos', 'vertUV')], index_buffer=indices)
        self.color_selection = "colorA"

    def update(self, _delta: float):
        if self.game.keyboard.just_pressed(pygame.K_F11):
            self.game.window.toggle_fullscreen()

        # change color selection
        if self.game.keyboard.just_pressed(pygame.K_1):
            self.color_selection = "colorA"
        if self.game.keyboard.just_pressed(pygame.K_2):
            self.color_selection = "colorB"

        mouse_pos = self.game.mouse.get_pos()

        # normalize cordinates
        off_x = mouse_pos[0] / self.game.window.current_size[0]
        off_y = mouse_pos[1] / self.game.window.current_size[1]

        # get actual value of colorA/colorB transform
        r, g, b, _ = self.program[self.color_selection].value
        color = f"{self.color_selection}({r:.1f}, {g:.1f}, {b:.1f})"
        self.game.set_title(f"Example WindowScreenGL {self.game.clock.get_fps():.0f} fps   {color}")

        # changing each color channel
        if self.game.keyboard.is_pressed(pygame.K_b):
            b = off_x * abs(off_y - 1)
        elif self.game.keyboard.is_pressed(pygame.K_r):
            r = off_x * abs(off_y - 1)
        elif self.game.keyboard.is_pressed(pygame.K_g):
            g = off_x * abs(off_y - 1)
        
        # changing colorA/colorB transform value
        if self.game.mouse.is_pressed(1):
            self.program[self.color_selection] = (r, g, b, 1.0)

        self.program["time"] = pgcrow.timers.TimeClock.seconds()

    def render_screen(self, _screen):
        self.ctx.clear(color=(0.1, 0.1, 0.14, 1.0))
        self.render_object.render(mode=moderngl.TRIANGLES)
        pygame.display.flip()


if __name__ == "__main__":
    app = MyGame()
    app.run()
