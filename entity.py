import pygame
from settings import ENTITY_START_RADIUS, GROWTH_RATE, ENEMY_START_SPEED, PLAYER_START_SPEED, SPEED_DECREASE_RATE, EAT_RATIO, WORLD_HEIGHT, WORLD_WIDTH

class Entity:
    def __init__(self, pos_x, pos_y, color, start_speed):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.radius = ENTITY_START_RADIUS 

        self.start_speed = start_speed
        self.speed = start_speed 
        self.vx = 0.0
        self.vy = 0.0

    def draw(self, surface):
        # teken entity als een cirkel
        pygame.draw.circle(surface, self.color, (int(self.pos_x), int(self.pos_y)), self.radius)

    def distance_to(self, other):
        # Bereken de afstand tussen deze entiteit en een andere entiteit
        dx = self.pos_x - other.pos_x
        dy = self.pos_y - other.pos_y
        return (dx**2 + dy**2) ** 0.5
    
    def eat_food(self, foods):
        # Controleer of deze entiteit voedsel kan eten
        for food in foods[:]:
            if self.distance_to(food) < self.radius + food.radius:
                # Eet het voedsel en vergroot de radius
                self.radius += GROWTH_RATE
                self.speed_decrease()  # Verminder de snelheid na het eten
                foods.remove(food)

    def can_eat_bot(self, other):
        # Controleer of deze entiteit een andere bot kan eten
        groot_genoeg = self.radius > other.radius * EAT_RATIO
        dichtbij_genoeg = self.distance_to(other) < self.radius + other.radius*0.2 
        return groot_genoeg and dichtbij_genoeg 
    
    def move(self):
        # Update de positie of staat van de entiteit hier
        pass

    def handle_borders(self):
    # Zorg ervoor dat de speler binnen de schermranden blijft
        if self.pos_x < self.radius:
            self.pos_x = self.radius
            self.vx *= -1 #draait snelheid om bij botsing met rand
        elif self.pos_x > WORLD_WIDTH - self.radius:
            self.pos_x = WORLD_WIDTH - self.radius
            self.vx *= -1 #draait snelheid om bij botsing met rand

        if self.pos_y < self.radius:
            self.pos_y = self.radius
            self.vy *= -1 #draait snelheid om bij botsing met rand
        elif self.pos_y > WORLD_HEIGHT - self.radius:
            self.pos_y = WORLD_HEIGHT - self.radius
            self.vy *= -1 #draait snelheid om bij botsing met rand
    

    def speed_decrease(self):
        # Verminder de snelheid van de entity als die groter wordt
        self.speed = self.start_speed / (1 + self.radius * SPEED_DECREASE_RATE)
        