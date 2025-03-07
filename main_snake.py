import pygame
import random

pygame.init()

# Constants
MOVE_DELAY = 250  # Movement delay in milliseconds
screen_width = 400
screen_height = 250

# Initialize screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snek')

# Colors
color = pygame.Color("#3B3B3B")  # Dark gray background

# Snake head
snakepiece_surf = pygame.Surface((20, 20))
snakepiece_surf.fill('Cyan')
snakepiece_rect = pygame.Rect(200, 125, 20, 20)

# Snake body
snake_body = [snakepiece_rect.copy()]

# Bait
def generate_bait():
    return pygame.Rect(
        random.randint(0, (screen_width // 20) - 1) * 20,
        random.randint(0, (screen_height // 20) - 1) * 20,
        20, 20
    )

bait_surf = pygame.Surface((20, 20))
bait_surf.fill('Green')
bait_rect = generate_bait()

# Movement flags
moving_up = False
moving_down = False
moving_right = False
moving_left = False
any_key_pressed = False  # New flag to track initial movement

# Game loop
clock = pygame.time.Clock()
counter = 0
game_active = True

while True:
    screen.fill(color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if not any_key_pressed:  # First key press
                any_key_pressed = True
            if event.key == pygame.K_RIGHT and not moving_left:
                moving_left = moving_down = moving_up = False
                moving_right = True
            elif event.key == pygame.K_LEFT and not moving_right:
                moving_down = moving_right = moving_up = False
                moving_left = True
            elif event.key == pygame.K_UP and not moving_down:
                moving_left = moving_down = moving_right = False
                moving_up = True
            elif event.key == pygame.K_DOWN and not moving_up:
                moving_left = moving_right = moving_up = False
                moving_down = True

    if game_active:
        # Control snake speed
        counter += clock.get_time()
        if counter >= MOVE_DELAY and any_key_pressed:  # Only move after first key press
            counter = 0

            # Move the snake
            new_head = snakepiece_rect.copy()

            if moving_up:
                new_head.move_ip(0, -20)
            elif moving_down:
                new_head.move_ip(0, 20)
            elif moving_right:
                new_head.move_ip(20, 0)
            elif moving_left:
                new_head.move_ip(-20, 0)

            # Check wall collision
            if (new_head.x < 0 or new_head.x >= screen_width or
                new_head.y < 0 or new_head.y >= screen_height):
                game_active = False

            # Check self-collision
            for segment in snake_body:
                if new_head.colliderect(segment):
                    game_active = False
                    break

            # Update snake body
            snake_body.insert(0, new_head)
            snakepiece_rect = new_head

            # Check bait collision
            if snakepiece_rect.colliderect(bait_rect):
                # Generate new bait not on snake
                while True:
                    new_bait = generate_bait()
                    if not any(segment.colliderect(new_bait) for segment in snake_body):
                        bait_rect = new_bait
                        break
            else:
                if len(snake_body) > 1:  # Prevent immediate self-collision
                    snake_body.pop()

        # Draw elements
        for segment in snake_body:
            screen.blit(snakepiece_surf, segment)
        screen.blit(bait_surf, bait_rect)

    pygame.display.flip()
    clock.tick(60)