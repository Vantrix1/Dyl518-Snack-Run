import pygame
import random
import sys

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
    img.set_colorkey((0, 0, 0))
    return pygame.transform.scale(img, size)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Digestive Collector")
clock = pygame.time.Clock()
dt = 0
running = True

font = pygame.font.SysFont("Arial", 24)
desc_font = pygame.font.SysFont("Arial", 20)
WHITE = (255, 255, 255)
DARK_GREY = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BG_COLOR = (30, 30, 30)

player_size = 64
player_speed = 300
player_image = load_image_scaled('player.bmp', (player_size, player_size))
player = GameObject(player_image, screen.get_width() // 2, screen.get_height() // 2)

def spawn_digestive():
    size = 25
    x = random.randint(0, screen.get_width() - size)
    y = random.randint(0, screen.get_height() - size)
    digestive_image = load_image_scaled('digestive.bmp', (size, size))
    return GameObject(digestive_image, x, y)

digestive = spawn_digestive()

money = 0
cash_multiplier = 1
upgrade_cost_multiplier = 50
upgrade_cost_speed = 100

multiplier_button = pygame.Rect(10, 50, 300, 40)
speed_button = pygame.Rect(10, 100, 300, 40)

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if multiplier_button.collidepoint(event.pos) and money >= upgrade_cost_multiplier:
                money -= upgrade_cost_multiplier
                cash_multiplier += 1
                upgrade_cost_multiplier = int(upgrade_cost_multiplier * 1.3)
            if speed_button.collidepoint(event.pos) and money >= upgrade_cost_speed:
                money -= upgrade_cost_speed
                player_speed += 50
                upgrade_cost_speed = int(upgrade_cost_speed * 1.3)

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

    if (player.pos.x < 0 or player.pos.x + player.rect.width > screen.get_width() or
        player.pos.y < 0 or player.pos.y + player.rect.height > screen.get_height()):
        print("You hit the wall! Game over.")
        pygame.quit()
        sys.exit()

    if player.rect.colliderect(digestive.rect):
        money += 10 * cash_multiplier
        digestive = spawn_digestive()

    screen.fill(BG_COLOR)
    player.draw(screen)
    digestive.draw(screen)

    pygame.draw.rect(screen, DARK_GREY, multiplier_button)
    pygame.draw.rect(screen, DARK_GREY, speed_button)
    pygame.draw.rect(screen, YELLOW, multiplier_button, 2)
    pygame.draw.rect(screen, CYAN, speed_button, 2)

    money_text = font.render(f"Money: ${money}", True, WHITE)
    multiplier_text = font.render(f"Snack Attack | ${upgrade_cost_multiplier}", True, YELLOW)
    speed_text = font.render(f"Sugar Rush | ${upgrade_cost_speed}", True, CYAN)

    screen.blit(money_text, (10, 10))
    screen.blit(multiplier_text, (15, 58))
    screen.blit(speed_text, (15, 108))

   
    if multiplier_button.collidepoint(mouse_pos):
        desc = desc_font.render(f"Permanent increase in digestive value.\nCurrent multiplier x{cash_multiplier}", True, LIGHT_GREY)
        screen.blit(desc, (320, 58))
    if speed_button.collidepoint(mouse_pos):
        desc = desc_font.render("Boosts player movement speed.", True, LIGHT_GREY)
        screen.blit(desc, (320, 108))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
