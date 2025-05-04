import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 1
ENEMY_ROWS = 3
ENEMY_COLS = 8
ENEMY_PADDING = 50
ENEMY_OFFSET_X = 100
ENEMY_OFFSET_Y = 50

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED * direction

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1  # 1 for right, -1 for left

    def update(self, enemies):
        self.rect.x += ENEMY_SPEED * self.direction
        # Check if enemies hit the edge
        if any(enemy.rect.right >= SCREEN_WIDTH or enemy.rect.left <= 0 for enemy in enemies):
            self.direction *= -1
            for enemy in enemies:
                enemy.rect.y += 20

# Create groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for row in range(ENEMY_ROWS):
    for col in range(ENEMY_COLS):
        enemy = Enemy(ENEMY_OFFSET_X + col * 60, ENEMY_OFFSET_Y + row * 40)
        enemies.add(enemy)
        all_sprites.add(enemy)

# Game variables
score = 0
game_over = False

# Main game loop
while not game_over:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top, -1)
                bullets.add(bullet)
                all_sprites.add(bullet)

    # Update
    player.update(keys)
    bullets.update()
    enemies.update(enemies)

    # Collision detection
    for bullet in bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        for enemy in hit_enemies:
            score += 10
            bullet.kill()

    # Check if enemies reach the bottom
    if any(enemy.rect.bottom >= SCREEN_HEIGHT for enemy in enemies):
        game_over = True

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    bullets.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

# Game over
print("Game Over!")
pygame.quit()
