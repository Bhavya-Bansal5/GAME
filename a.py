import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load sounds
catch_apple_sound = pygame.mixer.Sound("sounds/catch_apple.wav")
hit_bomb_sound = pygame.mixer.Sound("sounds/hit_bomb.wav")

# Load images
player_image = pygame.image.load("player.png").convert_alpha()
apple_image = pygame.image.load("apple.jpg").convert_alpha()
bomb_image = pygame.image.load("bomb.png").convert_alpha()
background_image = pygame.image.load("a.jpg").convert()  # Load the background image

# Resize images
player_image = pygame.transform.scale(player_image, (64, 64))  # Resize player to 64x64
apple_image = pygame.transform.scale(apple_image, (32, 32))    # Resize apple to 32x32
bomb_image = pygame.transform.scale(bomb_image, (32, 32))      # Resize bomb to 32x32
background_image = pygame.transform.scale(background_image, (800, 600))  
# Game variables
score = 0
game_time = 60
time_remaining = game_time
spawn_interval = 1000  # milliseconds
last_spawn_time = pygame.time.get_ticks()

# Player setup
player_rect = player_image.get_rect(center=(WIDTH // 2, HEIGHT - 50))

# Falling objects list (store tuples of (object_type, rect))
falling_objects = []

# Font setup
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += 5

    # Spawn falling objects
    if pygame.time.get_ticks() - last_spawn_time > spawn_interval:
        if random.choice([True, False]):
            falling_objects.append(("apple", apple_image.get_rect(center=(random.randint(50, WIDTH - 50), 0))))
        else:
            falling_objects.append(("bomb", bomb_image.get_rect(center=(random.randint(50, WIDTH - 50), 0))))
        last_spawn_time = pygame.time.get_ticks()

    # Move falling objects
    for obj in falling_objects[:]:
        obj_type, obj_rect = obj
        obj_rect.y += 5  # Move down

        # Check for collision with player
        if obj_rect.colliderect(player_rect):
            if obj_type == "apple":
                score += 1
                catch_apple_sound.play()
            else:
                score -= 1
                hit_bomb_sound.play()
            falling_objects.remove(obj)

        # Remove object if it falls below the screen
        if obj_rect.top > HEIGHT:
            falling_objects.remove(obj)

    # Update timer
    time_remaining -= clock.get_time() / 1000
    if time_remaining <= 0:
        running = False

    # Drawing
    screen.blit(background_image, (0, 0))  # Draw background
    for obj in falling_objects:
        obj_type, obj_rect = obj
        screen.blit(apple_image if obj_type == "apple" else bomb_image, obj_rect)
    screen.blit(player_image, player_rect)

    # Draw score and timer
    score_text = font.render(f"Score: {score}", True, GREEN)
    timer_text = font.render(f"Time: {int(time_remaining)}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (WIDTH - 100, 10))

    # Refresh screen
    pygame.display.flip()
    clock.tick(60)

# Game over
pygame.quit()
sys.exit()
