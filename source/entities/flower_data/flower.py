"""
Class Name: Flower
Class Purpose: Holds data common to all flowers
Notes:
"""

#  IMPORTS
from pygame import Vector2
from statistics import NormalDist

from source.entities.entity import Entity

random_gen = NormalDist(0.5, 0.15)  # This creates a normal distribution of range (0, 1)


def choose_color():
    """
    :return: A selection on a normal distribution of color
    """
    roll = random_gen.samples(1)[0]
    if 0.4 <= roll <= 0.6:
        return 0
    elif 0.3 < roll < 0.4:
        return 1
    elif 0.6 < roll < 0.7:
        return 3
    elif roll < 0.1 or roll > 0.9:
        return 2
    else:
        return 4


class Flower(Entity):

    # FUNCTIONS

    def __init__(self, location):
        self.busy = False  # Used by hives to designate orders
        self.pollen = 10  # How much pollen the flowers starts with
        self.neighbors = None  # Used for growth

        random_color = choose_color()

        Entity.__init__(self, location, 'flower'+"_"+str(random_color))

    @property
    def center_loc(self):
        """
        :return: Center of the flower
        """
        return Vector2(self.rect.left + self.rect.width / 2, self.rect.top + self.rect.height / 2)

    def transfer_pollen(self, limit, current):
        """
        Completes the harvesting process and gives back some amount of pollen
        :param limit: Max pollen the bee can hold
        :param current: How much pollen the bee currently has
        :return: How much pollen the bee took from the flower
        """
        wanted = limit - current
        if wanted <= self.pollen:
            pollen_taken = wanted
            self.pollen = self.pollen - pollen_taken
        else:
            pollen_taken = self.pollen
            self.pollen = 0

        return pollen_taken
