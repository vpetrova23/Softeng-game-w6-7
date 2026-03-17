from entity import Entity
from settings import PLAYER_START_RADIUS, PLAYER_COLOR
import pygame

class Player(Entity):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, color=PLAYER_COLOR, radius=PLAYER_START_RADIUS)

    def move(self):
        # Laat de speler de muis volgen
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.pos_x
        dy = mouse_y - self.pos_y

        self.pos_x += dx * 0.05      
        self.pos_y += dy * 0.05


    