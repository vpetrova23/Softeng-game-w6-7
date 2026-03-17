import pygame
from settings import PLAYER_START_RADIUS, GROWTH_RATE

class Entity:
    def __init__(self, pos_x, pos_y, color, radius=PLAYER_START_RADIUS):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.radius = radius


    def draw(self, surface):
        # teken entity als een cirkel
        pygame.draw.circle(surface, self.color, (self.pos_x, self.pos_y), self.radius)

    def distance_to(self, other):
        # Bereken de afstand tussen deze entiteit en een andere entiteit
        dx = self.pos_x - other.pos_x
        dy = self.pos_y - other.pos_y
        return (dx**2 + dy**2) ** 0.5
    
    def eat_food(self, foods):
        # Controleer of deze entiteit voedsel kan eten
        for food in foods:
            if self.distance_to(food) < self.radius + food.radius:
                # Eet het voedsel en vergroot de radius
                self.radius += GROWTH_RATE
                foods.remove(food)

    def can_eat_bot(self, other):
        # Controleer of deze entiteit een andere bot kan eten
        groot_genoeg = self.radius > other.radius * 1.1
        dichtbij_genoeg = self.distance_to(other) < self.radius + other.radius*0.2 
        return groot_genoeg and dichtbij_genoeg 
    
    def update(self):
        # Update de positie of staat van de entiteit hier
        pass

