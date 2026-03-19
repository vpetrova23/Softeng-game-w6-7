import pygame
from settings import WORLD_WIDTH, WORLD_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH

class Camera:
    """Beheert de camera die de speler volgt."""
    
    def __init__(self, player):
        self.player = player
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.x = 0  # Camera offset X
        self.y = 0  # Camera offset Y
        self.zoom = 1.0
    
    def update(self, player):
        """Update camera positie om speler in het midden te houden."""
        # Zorg dat speler in het midden van het scherm staat
        self.x = player.pos_x - self.screen_width // 2
        self.y = player.pos_y - self.screen_height // 2
        
        # Zorg dat camera niet buiten de wereld gaat
        self.x = max(0, min(self.x, WORLD_WIDTH - self.screen_width))
        self.y = max(0, min(self.y, WORLD_HEIGHT - self.screen_height))
    
    def get_screen_pos(self, world_x, world_y):
        """Zet wereld-coördinaten om naar scherm-coördinaten."""
        screen_x = world_x - self.x
        screen_y = world_y - self.y
        return (screen_x, screen_y)
    
    def is_visible(self, entity_x, entity_y, entity_radius):
        """Check of een entity zichtbaar is op het scherm."""
        screen_x, screen_y = self.get_screen_pos(entity_x, entity_y)
        # Check of entity op of dicht bij scherm is
        return (-entity_radius < screen_x < self.screen_width + entity_radius and
                -entity_radius < screen_y < self.screen_height + entity_radius)
    
    def draw_world(self, surface, world):
        """Teken alle wereld-entiteiten (voedsel en enemies) met camera offset."""
        # Teken voedsel
        for food in world.foods:
            if self.is_visible(food.x, food.y, food.radius):
                screen_x, screen_y = self.get_screen_pos(food.x, food.y)
                pygame.draw.circle(surface, food.color, (int(screen_x), int(screen_y)), food.radius)
        
        # Teken enemies
        for enemy in world.enemies:
            if self.is_visible(enemy.pos_x, enemy.pos_y, enemy.radius):
                screen_x, screen_y = self.get_screen_pos(enemy.pos_x, enemy.pos_y)
                pygame.draw.circle(surface, enemy.color, (int(screen_x), int(screen_y)), enemy.radius)
    
    def draw_entity(self, surface, entity):
        """Teken een entity (speler) via camera."""
        if self.is_visible(entity.pos_x, entity.pos_y, entity.radius):
            screen_x, screen_y = self.get_screen_pos(entity.pos_x, entity.pos_y)
            pygame.draw.circle(surface, entity.color, (int(screen_x), int(screen_y)), entity.radius)