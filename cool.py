import pygame
import random
import sys

# Define GameObject class
class GameObject:
    def __init__(self, image, x, y):
        self.image = image
        self.pos = pygame.Vector2(x, y)
        self.rect = self.image.get_rect(topleft=self.pos)

    def update_rect(self):
        self.rect.topleft = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.pos)

def load_image_scaled(path, size):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0, 0, 0))  # Optional: make black transparent
    return pygame.transform.scale(img, size)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Digestive Collector")
clock = pygame.time.Clock()
dt = 0
running = True

# Font for UI
font = pygame.font.SysFont("Arial", 30)

# Player setup
player_size = 64
player_speed = 300
player_image = load_image_scaled('player.bmp', (player_size, player_size))
player = GameObject(player_image, screen.get_width() // 2, screen.get_height() // 2)

# Digestive spawn function
def spawn_digestive():
    size = 25
    x = random.randint(0, screen.get_width() - size)
    y = random.randint(0, screen.get_height() - size)
    digestive_image = load_image_scaled('digestive.bmp', (size, size))
    return GameObject(digestive_image, x, y)

digestive = spawn_digestive()

# Currency and upgrades
money = 0
cash_multiplier = 1
upgrade_cost_multiplier = 50
upgrade_cost_speed = 100

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m and money >= upgrade_cost_multiplier:
                money -= upgrade_cost_multiplier
                cash_multiplier += 1
                upgrade_cost_multiplier = int(upgrade_cost_multiplier * 1.3)
            if event.key == pygame.K_n and money >= upgrade_cost_speed:
                money -= upgrade_cost_speed
                player_speed += 50
                upgrade_cost_speed = int(upgrade_cost_speed * 1.3)

    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.pos.y -= player_speed * dt
    if keys[pygame.K_s]:
        player.pos.y += player_speed * dt
    if keys[pygame.K_a]:
        player.pos.x -= player_speed * dt
    if keys[pygame.K_d]:
        player.pos.x += player_speed * dt

    player.update_rect()

    # Edge collision check


    # Digestive collision check
    if player.rect.colliderect(digestive.rect):
        money += 10 * cash_multiplier
        digestive = spawn_digestive()

    # Drawing
    screen.fill("green")
    player.draw(screen)
    digestive.draw(screen)

    # Draw UI
    money_text = font.render(f"Money: ${money}", True, (255, 255, 255))
    multiplier_text = font.render(f"Multiplier: x{cash_multiplier} (Press M: ${upgrade_cost_multiplier})", True, (255, 255, 0))
    speed_text = font.render(f"Speed: {player_speed} (Press N: ${upgrade_cost_speed})", True, (0, 255, 255))

    screen.blit(money_text, (10, 10))
    screen.blit(multiplier_text, (10, 50))
    screen.blit(speed_text, (10, 90))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()