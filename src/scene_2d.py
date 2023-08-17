"""## Scene 2D"""


class Scene2D:
    """Class representing a single game scene"""

    def __init__(self, game) -> None:
        self.game = game
        self.game.event_handler.loop = self.handle_events

    def handle_events(self):
        """Custom event handling method"""

    def update(self, dt: float):
        """For updating stuff"""

    def render(self):
        """For rendering stuff"""
