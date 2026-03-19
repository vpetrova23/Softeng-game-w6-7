import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BACKGROUND_COLOR
from player import Player
from world import World
from camera import Camera

class Game:
    """Hoofd game loop - beheert speler, wereld en camera."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Avar.io")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.player = Player()
        self.world = World()
        self.camera = Camera(self.player)
        self.name_font = pygame.font.SysFont("arial", 18, bold=True)

        
    def handle_events(self):
        """Handel input af."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        """Update speler en check collisions."""
        delta_tijd = self.clock.tick(FPS) / 1000.0
        
        # Update speler
        self.player.move(camera=self.camera)
        self.player.eat_food(self.world.foods)
        self.player.handle_borders()


    # Update wereld (enemies en voedsel)
        self.world.update(delta_tijd)
        
        # Update camera om speler te volgen
        self.camera.update(self.player)
        
        # Check of speler enemies kan eten
        for enemy in self.world.enemies[:]:
            if self.player.can_eat_bot(enemy):
                self.player.radius += enemy.radius * 0.5
                self.world.enemies.remove(enemy)
            elif enemy.can_eat_bot(self.player):
                self.game_over()
        
        # Respawn voedsel als nodig
        if len(self.world.foods) < 50:
            self.world.respawn_food()
    
    def draw(self):
        """Teken alles."""
        self.screen.fill(BACKGROUND_COLOR)

        # Teken wereld via camera (met offset)
        self.camera.draw_world(self.screen, self.world)
        
        # Teken speler via camera
        self.camera.draw_entity(self.screen, self.player)
        
        # Teken naam van speler
        screen_x, screen_y = self.camera.get_screen_pos(self.player.pos_x, self.player.pos_y)

        font_size = max(10, int(self.player.radius * 0.5)) # Pas fontgrootte aan op basis van radius
        name_font = pygame.font.SysFont("arial", font_size, bold=True)
        label = name_font.render(self.player.name, True, (20, 20, 20))
        label_rect = label.get_rect(center=(int(screen_x), int(screen_y)))  
        self.screen.blit(label, label_rect)
        
        pygame.display.flip()

    def run(self):
        """Hoofd game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()
    
    def game_over(self):
        """Spel is voorbij."""
        self.running = False


if __name__ == "__main__":
    game = Game()
    game.run()