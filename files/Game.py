import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.8  # Gravity for faster falling
FLAP_STRENGTH = -10  # Increased flap strength for more upward force
PIPE_WIDTH = 70
PIPE_GAP = 150

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # Yellow color for the bird
DARK_GREEN = (0, 150, 0)  # Darker green color for the pipes
BRIGHT_BLUE = (0, 191, 255)  # Bright blue color for the background
BLACK = (0, 0, 0)  # Black color for text

# Font
FONT = pygame.font.Font(None, 36)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = 30
        self.height = 30

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))  # Draw the bird as a yellow rectangle

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.passed = False

    def update(self):
        self.x -= 5

    def draw(self, screen):
        pygame.draw.rect(screen, DARK_GREEN, (self.x, 0, PIPE_WIDTH, self.height))  # Draw the top pipe as a darker green rectangle
        pygame.draw.rect(screen, DARK_GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))  # Draw the bottom pipe

# Main game function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True
    game_over = False

    while running:
        screen.fill(BRIGHT_BLUE)  # Set the background color to bright blue

        if not game_over:
            bird.update()
            bird.draw(screen)

            for pipe in pipes:
                pipe.update()
                pipe.draw(screen)

                # Check for collision
                if pipe.x < bird.x < pipe.x + PIPE_WIDTH and not pipe.passed:
                    if bird.y < pipe.height or bird.y + bird.height > pipe.height + PIPE_GAP:
                        game_over = True
                    if bird.x + bird.width > pipe.x and not pipe.passed:  # Check if the bird has passed the pipe
                        pipe.passed = True
                        score += 1  # Increment score when the bird successfully passes a pipe

            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())

            if pipes[0].x < -PIPE_WIDTH:
                pipes.pop(0)

            if bird.y > SCREEN_HEIGHT or bird.y < 0:
                game_over = True

            # Display the score
            score_text = FONT.render(f'Score: {score}', True, BLACK)
            screen.blit(score_text, (10, 10))  # Draw score in the top left corner

        else:
            # Game over screen
            game_over_text = FONT.render(f'Game Over! Score: {score}', True, BLACK)
            restart_text = FONT.render('Press R to Restart', True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if event.key == pygame.K_r and game_over:
                    # Reset the game
                    bird = Bird()
                    pipes = [Pipe()]
                    score = 0  # Reset score
                    game_over = False

    pygame.quit()

if __name__ == "__main__":
    main()
