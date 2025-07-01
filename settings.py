# Chapter 1 : A ship that firers bullets
""" We are creating a new file for settings class.
Each time we introduce new functionality into the game, we will typically create some new setting.
Instead of adding settings throughout the code, lets write a module called settings that contains
a class called settings that contains a class called 'Settings' to store all of these values in one place.
With this approach, we can use just one settings object anytime we need to access an individual setting.
This also makes it easier to modify the game's appearance and behavior as my project grows."""


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 5.0  # Speed of the Ship
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 5  # 8 or 10, experiment!
        self.bullet_height = 25  # or 30
        self.bullet_color = (255, 255, 255)  # WHITE
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1





