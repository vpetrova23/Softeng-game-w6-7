import pygame
from entity import Entity
import math 
import random
import colorsys
from settings import ENEMY_START_SPEED, ENEMY_CHASE_STRENGTH, ENEMY_START_VELOCITY_RANGE

def random_kleur(): # geeft random kleur aan enemies
    tint = random.random()
    verzadiging = random.uniform(0.78, 1.0)
    licht = random.uniform(0.92, 1.0)
    rood, groen, blauw = colorsys.hsv_to_rgb(tint, verzadiging, licht)
    return (int(rood * 255), int(groen * 255), int(blauw * 255))


class Enemy(Entity):
    def __init__(self, pos_x, pos_y):
        # Kies een willekeurige positie binnen de wereld
        super().__init__(pos_x, pos_y, color=random_kleur(), start_speed=ENEMY_START_SPEED)
        self.speed = ENEMY_START_SPEED
        self.vx = random.uniform(ENEMY_START_VELOCITY_RANGE[0], ENEMY_START_VELOCITY_RANGE[1])  
        self.vy = random.uniform(ENEMY_START_VELOCITY_RANGE[0], ENEMY_START_VELOCITY_RANGE[1])  

        

    def move(self, delta_tijd, foods, player):
        if self.can_see_bot(player):        # ziet speler en is groot genoeg: chase
            target = player
            flee = False
        elif player.can_see_bot(self):      # speler ziet enemy en is groot genoeg: vlucht
            target = player
            flee = True
        elif foods:
            target = min(foods, key=lambda food: self.distance_to(food))
            flee = False
        else:
            target = None
            flee = False


        if target is not None:
            dx = target.pos_x - self.pos_x
            dy = target.pos_y - self.pos_y
            distance = math.hypot(dx, dy)

            if distance > 0:
                dx /= distance
                dy /= distance

                if flee:
                    # Beweeg WEG van de speler (richting omdraaien)
                    self.vx = -dx * self.speed * ENEMY_CHASE_STRENGTH
                    self.vy = -dy * self.speed * ENEMY_CHASE_STRENGTH
                else:
                    self.vx = dx * self.speed * ENEMY_CHASE_STRENGTH
                    self.vy = dy * self.speed * ENEMY_CHASE_STRENGTH
        else:
            self.vx = 0.0
            self.vy = 0.0

        self.pos_x += self.vx * delta_tijd
        self.pos_y += self.vy * delta_tijd
        self.handle_borders()