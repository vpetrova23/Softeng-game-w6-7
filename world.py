import random
from settings import WORLD_WIDTH, WORLD_HEIGHT, FOOD_COUNT, ENEMY_COUNT, GROWTH_RATE, EAT_RATIO
from enemy import Enemy
from food import Food

class World:
    """Beheert de kaart, spawnt en update voedsel en enemies"""
    def __init__(self):
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT
        self.foods = []
        self.enemies = []
        self._spawn_foods()
        self._spawn_enemies()


    def _spawn_foods(self):
        """Spawn voedselbolletjes op willekeurige posities"""
        for _ in range(FOOD_COUNT):
            food = Food()
            self.foods.append(food)

    def _spawn_enemies(self):
        """Spawn enemies op willekeurige posities."""
        for _ in range(ENEMY_COUNT):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            enemy = Enemy(x, y)
            self.enemies.append(enemy)

    def respawn_food(self):
        """Spawn nieuw voedsel"""
        food = Food()
        self.foods.append(food)
    

    def update(self, delta_tijd):
        """Update voedsel en enemies"""
        # Update voedsel beweging
        for food in self.foods:
            food.move(delta_tijd)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.move(delta_tijd)
            enemy.eat_food(self.foods)
            enemy.handle_borders()
        
        # Controleer of enemies elkaar eten
        for i, enemy1 in enumerate(self.enemies):
            for enemy2 in self.enemies[i+1:]:
                if enemy1.can_eat_bot(enemy2):
                    enemy1.radius += enemy2.radius * GROWTH_RATE
                    self.enemies.remove(enemy2)
                elif enemy2.can_eat_bot(enemy1):
                    enemy2.radius += enemy1.radius * GROWTH_RATE
                    self.enemies.remove(enemy1)
                    break


    def draw(self, surface):
        """Teken voedsel en enemies"""
        for food in self.foods:
            food.draw(surface)  
        for enemy in self.enemies:
            enemy.draw(surface)