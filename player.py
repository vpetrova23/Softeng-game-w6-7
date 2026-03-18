from entity import Entity
from settings import PLAYER_START_RADIUS, PLAYER_COLOR, WORLD_HEIGHT, WORLD_WIDTH
import pygame
import math


class Player(Entity):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, color=PLAYER_COLOR, radius=PLAYER_START_RADIUS)

    def move(self):
        # Laat de speler de muis volgen
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.pos_x
        dy = mouse_y - self.pos_y

        distance = math.hypot(dx, dy)
        if distance > 0:
            # Richting normaliseren (dx, dy tussen -1 en 1)
            dx /= distance
            dy /= distance

            # Beweeg met de huidige speed
            self.pos_x += dx * self.speed
            self.pos_y += dy * self.speed
    

    def handle_borders(self):
        # Zorg ervoor dat de speler binnen de schermranden blijft
        if self.pos_x < self.radius:
            self.pos_x = self.radius
        elif self.pos_x > WORLD_WIDTH - self.radius:
            self.pos_x = WORLD_WIDTH - self.radius

        if self.pos_y < self.radius:
            self.pos_y = self.radius
        elif self.pos_y > WORLD_HEIGHT - self.radius:
            self.pos_y = WORLD_HEIGHT - self.radius


        