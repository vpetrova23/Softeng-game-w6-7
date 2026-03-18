import math
import random
import colorsys

import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 760
FPS = 60

WORLD_WIDTH = 5200
WORLD_HEIGHT = 5200
FOOD_TARGET_COUNT = 320
ENEMY_COUNT = 10

PLAYER_START_MASS = 225.0
ENEMY_MIN_MASS = 120.0
ENEMY_MAX_MASS = 420.0
MAX_FOOD_VALUE = 5.0


def clamp(value, low, high):
    return max(low, min(high, value))


def random_bright_color():
    hue = random.random()
    saturation = random.uniform(0.78, 1.0)
    value = random.uniform(0.92, 1.0)
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return (int(r * 255), int(g * 255), int(b * 255))


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.offset = pygame.Vector2(0, 0)

    def resize(self, width, height):
        self.width = width
        self.height = height

    def follow(self, target_position, world_width, world_height):
        self.offset.x = target_position.x - self.width / 2
        self.offset.y = target_position.y - self.height / 2
        self.offset.x = clamp(self.offset.x, 0, world_width - self.width)
        self.offset.y = clamp(self.offset.y, 0, world_height - self.height)

    def world_to_screen(self, world_position):
        return world_position - self.offset

    def screen_to_world(self, screen_position):
        return pygame.Vector2(screen_position) + self.offset


class Entity:
    def __init__(self, x, y, mass, color, name=""):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.mass = float(mass)
        self.color = color
        self.name = name

    @property
    def radius(self):
        return max(8.0, math.sqrt(self.mass))

    def speed(self):
        return 200 / (self.radius ** 0.58)

    def move(self, dt, world_width, world_height):
        self.position += self.velocity * dt
        self.position.x = clamp(self.position.x, self.radius, world_width - self.radius)
        self.position.y = clamp(self.position.y, self.radius, world_height - self.radius)

    def can_eat(self, other):
        return self.mass > other.mass * 1.12

    def overlaps_enough_to_eat(self, other):
        distance = self.position.distance_to(other.position)
        return distance < self.radius - other.radius * 0.2

    def draw(self, surface, camera, font):
        screen_pos = camera.world_to_screen(self.position)
        center = (int(screen_pos.x), int(screen_pos.y))
        pygame.draw.circle(surface, self.color, center, int(self.radius))
        pygame.draw.circle(surface, (20, 20, 20), center, int(self.radius), 2)

        if self.name:
            label = font.render(self.name, True, (20, 20, 20))
            label_rect = label.get_rect(center=center)
            surface.blit(label, label_rect)


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_START_MASS, (93, 198, 255), "Jij")

    def update(self, dt, world, camera):
        mouse_position = pygame.mouse.get_pos()
        target_world = camera.screen_to_world(mouse_position)
        to_target = target_world - self.position
        distance = to_target.length()

        if distance > 0:
            direction = to_target.normalize()
            speed = self.speed()
            if distance < 120:
                speed *= distance / 120
            self.velocity = direction * speed
        else:
            self.velocity.update(0, 0)

        self.move(dt, world.width, world.height)


class Enemy(Entity):
    def __init__(self, x, y, mass, color, name):
        super().__init__(x, y, mass, color, name)
        angle = random.uniform(0, math.tau)
        self.wander_direction = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.wander_time_left = random.uniform(0.35, 1.1)

    def update(self, dt, world):
        self.wander_time_left -= dt
        if self.wander_time_left <= 0:
            # Kies periodiek een nieuwe random richting.
            angle = random.uniform(0, math.tau)
            self.wander_direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            self.wander_time_left = random.uniform(0.35, 1.1)

        self.velocity = self.wander_direction * self.speed() * 0.9
        self.move(dt, world.width, world.height)


class Food:
    def __init__(self, x, y, value, color):
        self.position = pygame.Vector2(x, y)
        self.value = value
        self.radius = int(max(2, self.value + 1.5))
        self.color = color

    @classmethod
    def random(cls, world_width, world_height):
        x = random.uniform(0, world_width)
        y = random.uniform(0, world_height)
        value = random.uniform(1.8, MAX_FOOD_VALUE)
        color = (
            random.randint(120, 255),
            random.randint(120, 255),
            random.randint(120, 255),
        )
        return cls(x, y, value, color)

    def draw(self, surface, camera):
        screen_pos = camera.world_to_screen(self.position)
        pygame.draw.circle(surface, self.color, (int(screen_pos.x), int(screen_pos.y)), self.radius)


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = None
        self.enemies = []
        self.food = []
        self.reset()

    def reset(self):
        self.player = Player(self.width / 2, self.height / 2)
        self.enemies = []

        for i in range(ENEMY_COUNT):
            x = random.uniform(120, self.width - 120)
            y = random.uniform(120, self.height - 120)
            mass = random.uniform(ENEMY_MIN_MASS, ENEMY_MAX_MASS)
            color = random_bright_color()
            self.enemies.append(Enemy(x, y, mass, color, f"Bot {i + 1}"))

        self.food = [Food.random(self.width, self.height) for _ in range(FOOD_TARGET_COUNT)]

    def ensure_food(self):
        while len(self.food) < FOOD_TARGET_COUNT:
            self.food.append(Food.random(self.width, self.height))

    def eat_food(self, entity):
        eaten = []
        for pellet in self.food:
            if entity.position.distance_to(pellet.position) < entity.radius + pellet.radius:
                entity.mass += pellet.value
                eaten.append(pellet)

        if eaten:
            self.food = [pellet for pellet in self.food if pellet not in eaten]

    def resolve_eating(self):
        game_over = False
        surviving_enemies = []

        for enemy in self.enemies:
            if self.player.can_eat(enemy) and self.player.overlaps_enough_to_eat(enemy):
                self.player.mass += enemy.mass * 0.85
                continue

            if enemy.can_eat(self.player) and enemy.overlaps_enough_to_eat(self.player):
                game_over = True
                surviving_enemies.append(enemy)
                continue

            surviving_enemies.append(enemy)

        self.enemies = surviving_enemies

        i = 0
        while i < len(self.enemies):
            eater = self.enemies[i]
            j = i + 1

            while j < len(self.enemies):
                other = self.enemies[j]

                if eater.can_eat(other) and eater.overlaps_enough_to_eat(other):
                    eater.mass += other.mass * 0.85
                    self.enemies.pop(j)
                    continue

                if other.can_eat(eater) and other.overlaps_enough_to_eat(eater):
                    other.mass += eater.mass * 0.85
                    self.enemies.pop(i)
                    i -= 1
                    break

                j += 1

            i += 1

        return game_over


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Agar.io - Class Structuur")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("arial", 24)
        self.text_font = pygame.font.SysFont("arial", 18)

        self.world = World(WORLD_WIDTH, WORLD_HEIGHT)
        self.camera = Camera(*self.screen.get_size())
        self.game_over = False

    def restart(self):
        self.world.reset()
        self.game_over = False

    def handle_events(self):
        running = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.camera.resize(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.restart()

        return running

    def update(self, dt):
        self.world.player.update(dt, self.world, self.camera)

        for enemy in self.world.enemies:
            enemy.update(dt, self.world)

        self.world.eat_food(self.world.player)
        for enemy in self.world.enemies:
            self.world.eat_food(enemy)

        self.game_over = self.world.resolve_eating()
        self.world.ensure_food()

    def draw_grid(self):
        spacing = 80
        left = int(self.camera.offset.x // spacing) * spacing
        top = int(self.camera.offset.y // spacing) * spacing
        right = int(self.camera.offset.x + self.camera.width)
        bottom = int(self.camera.offset.y + self.camera.height)

        grid_color = (230, 236, 240)
        for x in range(left, right + spacing, spacing):
            start = self.camera.world_to_screen(pygame.Vector2(x, top))
            end = self.camera.world_to_screen(pygame.Vector2(x, bottom))
            pygame.draw.line(self.screen, grid_color, start, end, 1)

        for y in range(top, bottom + spacing, spacing):
            start = self.camera.world_to_screen(pygame.Vector2(left, y))
            end = self.camera.world_to_screen(pygame.Vector2(right, y))
            pygame.draw.line(self.screen, grid_color, start, end, 1)

    def draw_ui(self):
        score = int(self.world.player.mass - PLAYER_START_MASS)
        lines = [
            f"Score: {max(0, score)}",
            f"Massa: {int(self.world.player.mass)}",
            f"Enemies over: {len(self.world.enemies)}",
            "Besturing: beweeg met je muis",
        ]

        y = 10
        for line in lines:
            text = self.title_font.render(line, True, (30, 30, 30))
            self.screen.blit(text, (12, y))
            y += 28

        if self.game_over:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.screen.blit(overlay, (0, 0))

            title = self.title_font.render("Game Over", True, (255, 255, 255))
            detail = self.text_font.render("Druk op R om opnieuw te starten", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.camera.width // 2, self.camera.height // 2 - 20))
            detail_rect = detail.get_rect(center=(self.camera.width // 2, self.camera.height // 2 + 14))

            self.screen.blit(title, title_rect)
            self.screen.blit(detail, detail_rect)

    def draw(self):
        self.screen.fill((245, 249, 251))
        self.draw_grid()

        for pellet in self.world.food:
            pellet.draw(self.screen, self.camera)

        for enemy in self.world.enemies:
            enemy.draw(self.screen, self.camera, self.text_font)

        self.world.player.draw(self.screen, self.camera, self.text_font)
        self.draw_ui()

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            running = self.handle_events()

            if not self.game_over:
                self.update(dt)

            self.camera.follow(self.world.player.position, self.world.width, self.world.height)
            self.draw()

        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
