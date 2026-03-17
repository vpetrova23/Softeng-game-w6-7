import random
import pygame
import colorsys
from settings import WORLD_WIDTH, WORLD_HEIGHT, FOOD_RADIUS

# Hulpfunctie voor random pastelkleuren 

def random_pastel_kleur():
    tint = random.random()  # tint tussen 0 en 1
    verzadiging = 0.2 + random.random() * 0.2  # Saturation tussen 0.5 en 1
    licht = 0.9 + random.random() * 0.1  # Value tussen 0.7 en 1
    rood, groen, blauw = colorsys.hsv_to_rgb(tint, verzadiging, licht)
    return (int(rood * 255), int(groen * 255), int(blauw * 255))


class Food:
    def __init__(self):
        self.x = random.randint(0, WORLD_WIDTH - 1)
        self.y = random.randint(0, WORLD_HEIGHT - 1)
        self.radius = FOOD_RADIUS
        self.color = random_pastel_kleur()
        self.vx = random.uniform(-25.0, 25.0) # geeft random startsnelheid
        self.vy = random.uniform(-25.0, 25.0) # geeft random startsnelheid

    # laat het voedsel random langzaam bewegen door de wereld
    def move(self, delta_tijd):
        self.vx += random.uniform(-10, 10) * delta_tijd
        self.vy += random.uniform(-10, 10) * delta_tijd

        max_snelheid = 40.0 # begrenst snelheid
        self.vx = max(-max_snelheid, min(max_snelheid, self.vx))
        self.vy = max(-max_snelheid, min(max_snelheid, self.vy))

        # werkelijke verplaatsing (snelheid * tijd)
        self.x += self.vx * delta_tijd  
        self.y += self.vy * delta_tijd 

        self.handle_borders()  # Zorg ervoor dat voedsel binnen de wereld blijft
    
    def handle_borders(self):
        if self.x < self.radius: # checkt linkerkant 
            self.x = self.radius
            self.vx *= -1 #draait snelheid om bij botsing met rand
        elif self.x > WORLD_WIDTH - self.radius: # checkt rechterkant
            self.x = WORLD_WIDTH - self.radius
            self.vx *= -1 #draait snelheid om bij botsing met rand
        
        if self.y < self.radius: # checkt bovenkant
            self.y = self.radius
            self.vy *= -1 #draait snelheid om bij botsing met rand
        elif self.y > WORLD_HEIGHT - self.radius: # checkt onderkant    
            self.y = WORLD_HEIGHT - self.radius
            self.vy *= -1 #draait snelheid om bij botsing met rand  
        
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (float(self.x), float(self.y)), self.radius)