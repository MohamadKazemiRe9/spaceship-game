class Settings:
    def __init__(self):
        self.bg_color = (14,3,20)
        self.screen_width = 1200
        self.screen_height = 800
        #bullet settings

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,165,0)
        self.bullet_allowed = 5

        #alien settings
        self.fleet_drop_speed = 10
        self.ship_limit = 3
        self.speedup_scale = 1.1

        self.iniatialize_daynamic_settings()

    def iniatialize_daynamic_settings(self):
        self.alien_speed = 1
        self.bullet_speed = 3
        self.ship_speed = 1.5
        self.fleet_direction = 1
        self.alien_point = 50

    def increae_speed(self):
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.alien_point = int(self.alien_point * self.speedup_scale)