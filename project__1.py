import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Collision Game")

# Colors
WHITE = (255, 255, 255)

# --- Load Sprites ---
# Replace 'player.png' and 'enemy.png' with your actual image file paths if different
try:
    player_img = pygame.image.load('player.png')
    enemy_img = pygame.image.load('enemy.png')
except pygame.error as e:
    print(f"Error loading images: {e}")
    # Create placeholder surfaces if images are missing
    player_img = pygame.Surface((32, 32))
    player_img.fill((0, 0, 255)) # Blue player
    enemy_img = pygame.Surface((32, 32))
    enemy_img.fill((255, 0, 0)) # Red enemy

# --- Game Variables ---
score = 0
font = pygame.font.Font(None, 36)
NUM_ENEMIES = 7

# Function to check collision (simple bounding box method)
def is_collision(sprite1_rect, sprite2_rect):
    return sprite1_rect.colliderect(sprite2_rect)

# --- Player Setup ---
player_rect = player_img.get_rect()
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
player_speed = 5

# --- Enemy Setup (7 enemies, positioned randomly) ---
enemies = []
for _ in range(NUM_ENEMIES):
    enemy_rect = enemy_img.get_rect()
    enemy_rect.x = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
    enemy_rect.y = random.randint(0, SCREEN_HEIGHT // 2 - enemy_rect.height)
    # Store the rect object for movement and collision detection
    enemies.append(enemy_rect)

# --- Main Game Loop ---
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
        player_rect.x += player_speed
    
    # Simple enemy movement (just to make the game dynamic)
    for enemy_rect in enemies:
        enemy_rect.y += 1 # Move enemies down slowly
        if enemy_rect.top > SCREEN_HEIGHT:
            # Respawn at top if they go off screen
            enemy_rect.y = 0 - enemy_rect.height
            enemy_rect.x = random.randint(0, SCREEN_WIDTH - enemy_rect.width)

    # --- Collision Detection and Score Increase ---
    for enemy_rect in enemies:
        if is_collision(player_rect, enemy_rect):
            score += 1
            # Optional: Respawn the hit enemy to continue the game
            enemy_rect.y = 0 - enemy_rect.height
            enemy_rect.x = random.randint(0, SCREEN_WIDTH - enemy_rect.width)
            # A visual indicator in the console that a collision happened
            print(f"Collision detected! Score: {score}")


    # --- Drawing ---
    screen.fill((0, 0, 0)) # Clear screen with black

    # Draw player and enemies
    screen.blit(player_img, player_rect)
    for enemy_rect in enemies:
        screen.blit(enemy_img, enemy_rect)

    # Draw score text
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
