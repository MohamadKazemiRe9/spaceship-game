class GameStats:
    def __init__(self,ai_game):
        self.settings = ai_game.settings
        self._reset_stats()
        self.hight_score = 0

    def _reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1