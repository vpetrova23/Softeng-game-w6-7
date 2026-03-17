import pygame
from settings import PLAYER_START_RADIUS

class Entity:
    def __init__(self, pos_x, pos_y, color, radius=PLAYER_START_RADIUS):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.radius = radius


    def draw(self, surface):
        # teken entity als een cirkel
        pygame.draw.circle(surface, self.color, (self.pos_x, self.pos_y), self.radius)


    def update(self):
        # Update de positie of staat van de entiteit hier
        pass

