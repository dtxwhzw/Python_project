"""Class for representing a Player entity within the game."""

__version__ = "1.1.0"

from game.entity import DynamicEntity

class Player(DynamicEntity):
    """A player in the game
    i write four new instances in this class
    the set_invincible, get_invincible, set powerup and get powerup
    they will be used when the player hit the star or flower.
    """
    _type = 3

    def __init__(self, name: str = "Mario", max_health: float = 20):
        """Construct a new instance of the player.

        Parameters:
            name (str): The player's name
            max_health (float): The player's maximum & starting health
        """
        super().__init__(max_health=max_health)

        self._invincible = False
        self._powerup = False
        self._name = name
        self._score = 0

    def get_name(self) -> str:
        """(str): Returns the name of the player."""
        return self._name

    def get_score(self) -> int:
        """(int): Get the players current score."""
        return self._score

    def change_score(self, change: float = 1):
        """Increase the players score by the given change value."""
        self._score += change

    def set_invincible(self, invincible: bool):
        self._invincible = invincible

    def get_invincible(self):
        return self._invincible

    def set_powerup(self, powerup: bool):
        self._powerup = powerup

    def get_powerup(self):
        return self._powerup

    # def fire(self, data):
    #     if self._powerup:
    #         world, mob = data
    #         x, y = self.get_position()
    #         drop = Fireball()
    #         world.add_mob(drop, x, y )
    #     else:
    #         pass

    def __repr__(self):
        return f"Player({self._name!r})"

