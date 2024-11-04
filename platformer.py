import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player properties
player_width = 50
player_height = 60
player_pos = [WIDTH // 2, HEIGHT - player_height - 10]
player_speed = 5
player_jump_speed = -15
gravity = 0.8
jumping = False
y_velocity = 0

# Platform properties
platforms = [
    pygame.Rect(100, 500, 200, 20),
    pygame.Rect(400, 400, 200, 20),
    pygame.Rect(200, 300, 150, 20),
    pygame.Rect(600, 200, 150, 20)
]

# Item properties
items = [pygame.Rect(random.randint(0, WIDTH - 20), random.randint(0, HEIGHT - 20), 20, 20) for _ in range(5)]

# Score
score = 0
font = pygame.font.SysFont("comicsansms", 30)

# Game clock
clock = pygame.time.Clock()

def draw_platforms():
    for platform in platforms:
        pygame.draw.rect(screen, BLUE, platform)

def draw_items():
    for item in items:
        pygame.draw.rect(screen, GREEN, item)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Horizontal movement
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_width:
        player_pos[0] += player_speed

    # Jumping logic
    if not jumping:
        if keys[pygame.K_SPACE]:
            jumping = True
            y_velocity = player_jump_speed

    # Gravity effect
    if jumping:
        player_pos[1] += y_velocity
        y_velocity += gravity

    # Check for collision with platforms
    on_ground = False
    for platform in platforms:
        if player_pos[1] + player_height <= platform.y and player_pos[1] + player_height + y_velocity >= platform.y and \
           platform.x < player_pos[0] < platform.x + platform.width or \
           platform.x < player_pos[0] + player_width < platform.x + platform.width:
            y_velocity = 0
            jumping = False
            player_pos[1] = platform.y - player_height
            on_ground = True

    # If not on any platform, apply gravity
    if not on_ground and not jumping:
        jumping = True
        y_velocity = gravity

    # Collision with items
    for item in items[:]:
        if pygame.Rect(player_pos[0], player_pos[1], player_width, player_height).colliderect(item):
            items.remove(item)
            score += 10

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (player_pos[0], player_pos[1], player_width, player_height))
    draw_platforms()
    draw_items()

    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
