import pygame
import math
import random
from fysom import *


class Bee(pygame.sprite.DirtySprite):
########################################################################################################################
    # Class Fields

    left_sprite = pygame.image.load("assets/bee_sprites/beeSprite_left.png")
    right_sprite = pygame.image.load("assets/bee_sprites/beeSprite_right.png")
    up_sprite = pygame.image.load("assets/bee_sprites/beeSprite_up.png")
    down_sprite = pygame.image.load("assets/bee_sprites/beeSprite_down.png")

    search_radius = 300
    wiggle = 1
    speed = 4
    roam_percentages = (0.64, 0.36)

########################################################################################################################

    def __init__(self, location, queen, bee_type):

        self.queen_hive = queen
        self.queen_hive_x = queen.rect.left + 33
        self.queen_hive_y = queen.rect.top + 52
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/bee_sprites/beeSprite_down.png")
        self.scouting_complete = True
        self.target_destination = (self.queen_hive_x, self.queen_hive_y)
        self.load_caste(bee_type)
        self.remembered_flower = None
        self.current_nectar = 0
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.random_spin_affinity = random.randint(0, 1)

    def load_caste(self, caste):
        if caste == "worker":
            self.bee_states = Fysom({
                # await orders > harvest > offload >...
                'initial': 'await orders',
                'events': [
                    {'name': 'go to flower', 'src': 'await orders', 'dst': 'harvest'},
                    {'name': 'harvest complete', 'src': 'harvest', 'dst': 'offload'},
                    {'name': 'offload complete', 'src': 'offload', 'dst': 'await orders'}
                ]
            })
        elif caste == "scout":
            self.bee_states = Fysom({
                # scout > report > dance >...
                'initial': 'scout',
                'events': [
                    {'name': 'begin search', 'src': 'dance', 'dst': 'scout'},
                    {'name': 'found flower', 'src': 'scout', 'dst': 'report'},
                    {'name': 'dance complete', 'src': 'report', 'dst': 'scout'}
                ]
            })

########################################################################################################################

    def move(self):
        self.target_destination = self.update_target(self.bee_states.current)
        self.head_towards()
        self.update_sprite()

    def update_target(self, origin_state):
        return {
            'await orders': self.check_available_orders(),
            'harvest': self.target_destination,
            'scout': self.search_for_flowers(),
            'offload': self.go_to_hive(),
            'report': self.go_to_hive(),
        }[origin_state]

    def go_to_hive(self):
        if self.bee_states.current == 'report' and \
                self.queen_hive_x - 10 < self.rect.left < self.queen_hive_x + 10 and \
                self.queen_hive_y - 10 < self.rect.top < self.queen_hive_y + 10:
            self.arrive_at_hive()

        return self.queen_hive_x, self.queen_hive_y

    def search_for_flowers(self):

        if self.scouting_complete:
            return self.begin_new_scouting_mission()
        else:
            if abs(self.target_destination[0] - self.rect.left) < 20:
                self.scouting_complete = True

            return self.target_destination

    def begin_new_scouting_mission(self):

        r = self.search_radius * math.sqrt(random.random())
        theta = random.random() * 2 * math.pi
        if random.randint(0, 1) == 0:
            random_x_coordinate = self.queen_hive_x + (r * math.cos(theta))
        else:
            random_x_coordinate = self.queen_hive_x - (r * math.cos(theta))
        if random.randint(0, 1) == 1:
            random_y_coordinate = self.queen_hive_y + (r * math.sin(theta))
        else:
            random_y_coordinate = self.queen_hive_y - (r * math.sin(theta))

        self.scouting_complete = False
        return random_x_coordinate, random_y_coordinate

    def head_towards(self):

        x_distance = self.target_destination[0] - (self.rect.left + 5)
        y_distance = self.target_destination[1] - (self.rect.top + 4)

        dx = 0
        dy = 0

        movement_points_to_spend = self.speed

        while True:
            if movement_points_to_spend == 0:
                break
            coin_flip = random.randint(0, 1)
            if coin_flip == 0:
                dx = dx + 1
            else:
                dy = dy + 1

            movement_points_to_spend = movement_points_to_spend - 1

        if x_distance < 0:
            dx = -dx
        if y_distance < 0:
            dy = -dy

        if -4 < x_distance < 4:
            dx = 0
        if -4 < y_distance < 4:
            dy = 0

        random_x_offset = random.randint(-self.wiggle, self.wiggle)
        random_y_offset = random.randint(-self.wiggle, self.wiggle)
        self.rect.top = self.rect.top + dy + random_x_offset
        self.rect.left = self.rect.left + dx + random_y_offset

    def check_available_orders(self):
        if self.queen_hive.has_orders() and self.bee_states.current == 'await orders':
            self.bee_states.trigger('go to flower')
            return self.queen_hive.get_order()
        else:
            return self.orbit_hive()

    def orbit_hive(self):

        angle = 0.36  # Magic Number - tune for speed of orbit

        random_x_offset = random.randint(-2, 2)
        random_y_offset = random.randint(-2, 2)

        ox = self.queen_hive_x
        oy = self.queen_hive_y

        px, py = self.rect.left, self.rect.top

        if self.random_spin_affinity == 0:
            qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        else:
            qx = ox + math.cos(-angle) * (px - ox) - math.sin(-angle) * (py - oy)
            qy = oy + math.sin(-angle) * (px - ox) + math.cos(-angle) * (py - oy)

        shipBack = (qx + random_x_offset, qy + random_y_offset)
        return shipBack

########################################################################################################################

    def update_sprite(self):

        x_distance = self.target_destination[0] - self.rect.left
        y_distance = self.target_destination[1] - self.rect.top

        if abs(x_distance) > abs(y_distance):
            if x_distance < 0:
                self.image = self.left_sprite
            else:
                self.image = self.right_sprite
        else:
            if y_distance < 0:
                self.image = self.up_sprite
            else:
                self.image = self.down_sprite

    def arrive_at_hive(self):
        self.scouting_complete = True
        self.bee_states.trigger('dance complete')
        self.queen_hive.remember_flower(self.remembered_flower)
        self.remembered_flower = None

    def validate_collision(self):
        if self.bee_states.current == 'scout' or self.bee_states.current == 'go to flower':
            return True
        else:
            return False

    def collide_with_flower(self, flower):
        if self.bee_states.current == 'scout':
            self.bee_states.trigger('found flower')
            self.remembered_flower = flower
        if self.bee_states.current == 'go to flower':
            self.bee_states.trigger('arrived at flower')
