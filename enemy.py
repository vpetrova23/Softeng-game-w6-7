import pygame
from entity import Entity
import math 
import random
import colorsys
from settings import ENEMY_START_SPEED, ENEMY_CHASE_STRENGTH, ENEMY_START_VELOCITY_RANGE

def random_kleur():
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

        

    def move(self, delta_tijd, foods):
        if foods:
            target = min(foods, key=lambda food: self.distance_to(food))
            dx = target.pos_x - self.pos_x
            dy = target.pos_y - self.pos_y
            distance = math.hypot(dx, dy)

            if distance > 0:
                dx /= distance
                dy /= distance 

                self.vx = dx * self.speed * ENEMY_CHASE_STRENGTH
                self.vy = dy * self.speed * ENEMY_CHASE_STRENGTH

        # werkelijke verplaatsing (snelheid * tijd)
        self.pos_x += self.vx * delta_tijd  
        self.pos_y += self.vy * delta_tijd 

        self.handle_borders()  # Zorg ervoor dat voedsel binnen de wereld blijft