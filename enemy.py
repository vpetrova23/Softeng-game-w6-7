import pygame
from entity import Entity
import math 
import random
import colorsys
from settings import ENEMY_START_SPEED, ENEMY_START_RADIUS

def random_kleur():
    tint = random.random()
    verzadiging = random.uniform(0.78, 1.0)
    licht = random.uniform(0.92, 1.0)
    rood, groen, blauw = colorsys.hsv_to_rgb(tint, verzadiging, licht)
    return (int(rood * 255), int(groen * 255), int(blauw * 255))


class Enemy(Entity):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, color=random_kleur())
        self.x = pos_x
        self.y = pos_y


    def move(self, delta_tijd):
        self.vx += random.uniform(-20, 20) * delta_tijd
        self.vy += random.uniform(-20, 20) * delta_tijd



        # werkelijke verplaatsing (snelheid * tijd)
        self.x += self.vx * delta_tijd  
        self.y += self.vy * delta_tijd 

        self.handle_borders()  # Zorg ervoor dat voedsel binnen de wereld blijft