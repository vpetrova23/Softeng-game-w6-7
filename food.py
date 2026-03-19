import random
import pygame
import colorsys
from settings import WORLD_WIDTH, WORLD_HEIGHT, FOOD_RADIUS, FOOD_ACCEL_RANGE, FOOD_MOVE

# Hulpfunctie voor random pastelkleuren 

def random_pastel_kleur():
    tint = random.random()  # tint tussen 0 en 1
    verzadiging = 0.2 + random.random() * 0.2  # Saturation tussen 0.5 en 1
    licht = 0.9 + random.random() * 0.1  # Value tussen 0.7 en 1
    rood, groen, blauw = colorsys.hsv_to_rgb(tint, verzadiging, licht)
    return (int(rood * 255), int(groen * 255), int(blauw * 255))


class Food:
    def __init__(self):
        self.pos_x = random.randint(0, WORLD_WIDTH - 1)
        self.pos_y = random.randint(0, WORLD_HEIGHT - 1)
        self.radius = FOOD_RADIUS
        self.color = random_pastel_kleur()
        self.vx = random.uniform(FOOD_ACCEL_RANGE[0], FOOD_ACCEL_RANGE[1]) # geeft random startsnelheid
        self.vy = random.uniform(FOOD_ACCEL_RANGE[0], FOOD_ACCEL_RANGE[1]) # geeft random startsnelheid

    # laat het voedsel random langzaam bewegen door de wereld
    def move(self, delta_tijd):
        self.vx += random.uniform(FOOD_MOVE[0], FOOD_MOVE[1]) * delta_tijd
        self.vy += random.uniform(FOOD_MOVE[0], FOOD_MOVE[1]) * delta_tijd

        max_snelheid = 40.0 # begrenst snelheid
        self.vx = max(-max_snelheid, min(max_snelheid, self.vx))
        self.vy = max(-max_snelheid, min(max_snelheid, self.vy))

        # werkelijke verplaatsing (snelheid * tijd)
        self.pos_x += self.vx * delta_tijd  
        self.pos_y += self.vy * delta_tijd

        self.handle_borders()  # Zorg ervoor dat voedsel binnen de wereld blijft
    
    def handle_borders(self):
        if self.pos_x < self.radius:  # checkt linkerkant
            self.pos_x = self.radius
            self.vx *= -1  # draait snelheid om bij botsing met rand
        elif self.pos_x > WORLD_WIDTH - self.radius:  # checkt rechterkant
            self.pos_x = WORLD_WIDTH - self.radius
            self.vx *= -1  # draait snelheid om bij botsing met rand

        if self.pos_y < self.radius:  # checkt bovenkant
            self.pos_y = self.radius
            self.vy *= -1  # draait snelheid om bij botsing met rand
        elif self.pos_y > WORLD_HEIGHT - self.radius:  # checkt onderkant
            self.pos_y = WORLD_HEIGHT - self.radius
            self.vy *= -1  # draait snelheid om bij botsing met rand

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (float(self.pos_x), float(self.pos_y)), self.radius)