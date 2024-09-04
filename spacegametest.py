import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 600  # Increased the width from 400 to 500
screen_height = 500

# Set up display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooters Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Load sounds
explosion_sound = pygame.mixer.Sound('bg.wav')

# Load images
player_image = pygame.image.load('player1.png')
enemy1_image = pygame.image.load('enemy1.png')
laser_image = pygame.image.load('laser.png')

# Scale images
player_image = pygame.transform.scale(player_image, (75, 50))
enemy1_image = pygame.transform.scale(enemy1_image, (75, 50))
laser_image = pygame.transform.scale(laser_image, (10, 20))

# Sprite classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 335

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy1_image
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 65

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = laser_image
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 200
        self.velocity = 0

    def update(self):
        self.rect.y += self.velocity

# Initialize player, enemy, and laser
player = Player()
enemy1 = Enemy()
laser = Laser()

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy1)
all_sprites.add(laser)

# Game variables
score = 0
font = pygame.font.Font(None, 25)
running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player.rect.x -= 10
    if keys[pygame.K_RIGHT]:
        player.rect.x += 10
    if keys[pygame.K_SPACE]:
        laser.velocity = -10
        laser.rect.x = player.rect.x + player.rect.width // 2 - laser.rect.width // 2
        laser.rect.y = player.rect.y - laser.rect.height
        explosion_sound.play()

    laser.update()

    # Check for collision
    if pygame.sprite.collide_rect(laser, enemy1):
        enemy1.rect.x = random.randint(20, 280)
        enemy1.rect.y = random.randint(20, 200)
        score += 5
    
    # Check for win condition
    if score > 149:
        player.kill()
        enemy1.kill()
        win_text = font.render("You Win!", True, GREEN)
        screen.blit(win_text, (screen_width // 2 - 50, screen_height // 2))

    # Drawing
    screen.fill(BLACK)
    
    # Draw text
    instructions = [
        "Space = Shoot", 
        "LEFT ARROW = Move Left", 
        "RIGHT ARROW = Move Right", 
        f"Score: {score}"
    ]
    for i, text in enumerate(instructions):
        rendered_text = font.render(text, True, GREEN if i == 3 else YELLOW)
        screen.blit(rendered_text, (10, 350 + i * 20))
    
    # Draw yellow ellipses
    ellipses = [(160, 54), (156, 135), (80, 269), (300, 257), (206, 337), (88, 41), (320, 150)]
    for ellipse_pos in ellipses:
        pygame.draw.ellipse(screen, YELLOW, (*ellipse_pos, 15, 15))

    # Draw sprites
    all_sprites.draw(screen)
    
    # Update display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(30)

pygame.quit()
