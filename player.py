from entity import Entity
from settings import ENTITY_START_RADIUS, PLAYER_COLOR, WORLD_HEIGHT, WORLD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
import math


class Player(Entity):
    def __init__(self):
        pos_x = WORLD_WIDTH // 2
        pos_y = WORLD_HEIGHT // 2
        super().__init__(pos_x, pos_y, color=PLAYER_COLOR)

        # Start snelheid is 0 omdat de speler alleen beweegt als de muis beweegt
        self.vx = 0.0
        self.vy = 0.0  

    def move(self):
        # Laat de speler de muis volgen
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - SCREEN_WIDTH / 2  # Bereken de afstand van de muis tot het midden van het scherm
        dy = mouse_y - SCREEN_HEIGHT / 2

        distance = math.hypot(dx, dy)
        if distance > 0:
            # Richting normaliseren (dx, dy tussen -1 en 1)
            dx /= distance
            dy /= distance

            # Beweeg met de huidige speed
            self.vx = dx * self.speed
            self.vy = dy * self.speed
        else:
            # als er geen beweging is, zet snelheid op 0
            self.vx = 0.0
            self.vy = 0.0
        
        self.pos_x += self.vx
        self.pos_y += self.vy  
        self.handle_borders()  # Zorg ervoor dat de speler binnen de wereld blijft

   
       


        