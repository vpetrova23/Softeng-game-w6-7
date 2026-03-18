import pygame
from settings import PLAYER_START_RADIUS, GROWTH_RATE, SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_START_SPEED, PLAYER_COLOR, SPEED_DECREASE_RATE

class Entity:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = PLAYER_COLOR
        self.radius = PLAYER_START_RADIUS
        self.speed = PLAYER_START_SPEED


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
    
    def move(self):
        # Update de positie of staat van de entiteit hier
        pass

    def handle_borders(self):
    # Zorg ervoor dat de speler binnen de schermranden blijft
        if self.pos_x < self.radius:
            self.pos_x = self.radius
        elif self.pos_x > SCREEN_WIDTH - self.radius:
            self.pos_x = SCREEN_WIDTH - self.radius

        if self.pos_y < self.radius:
            self.pos_y = self.radius
        elif self.pos_y > SCREEN_HEIGHT - self.radius:
            self.pos_y = SCREEN_HEIGHT - self.radius

    def speed_decrease(self):
        # Verminder de snelheid van de entity als die groter wordt
        self.speed = PLAYER_START_SPEED / (1 + self.radius * SPEED_DECREASE_RATE)
        