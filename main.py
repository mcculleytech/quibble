import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BG_COLOR = (0, 0, 0)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (255, 255, 255)
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 7
        self.target_y = None

    def move(self, up=True, down=False):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        if down and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def ai_move(self):
        if self.target_y is None:
            return
        if self.rect.centery < self.target_y:
            self.rect.y += self.speed
        elif self.rect.centery > self.target_y:
            self.rect.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect)


class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = random.choice([-4, 4])
        self.speed_y = random.choice([-4, 4])

    def move(self, paddle_left, paddle_right):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Wall collision (top and bottom)
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        # Paddle collision
        if self.rect.colliderect(paddle_left.rect) or self.rect.colliderect(
            paddle_right.rect
        ):
            self.speed_x *= -1

    def reset(self, x, y):
        self.rect.center = (x, y)
        self.speed_x = random.choice([-4, 4])
        self.speed_y = random.choice([-4, 4])

    def draw(self, screen):
        pygame.draw.ellipse(screen, BALL_COLOR, self.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    player_paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ai_paddle = Paddle(
        SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    )
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    player_score = 0
    ai_score = 0
    update_counter = 0

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Game Logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_paddle.move(up=True, down=False)
        elif keys[pygame.K_s]:
            player_paddle.move(up=False, down=True)

        # AI Reaction Delay & Randomized Target
        update_counter += 1
        if update_counter % 30 == 0:
            ai_paddle.target_y = ball.rect.centery + random.randint(-30, 30)

        ai_paddle.ai_move()
        ball.move(player_paddle, ai_paddle)

        # Scoring logic
        if ball.rect.left <= 0:
            ai_score += 1
            ball.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        elif ball.rect.right >= SCREEN_WIDTH:
            player_score += 1
            ball.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # 3. Rendering
        screen.fill(BG_COLOR)
        player_paddle.draw(screen)
        ai_paddle.draw(screen)
        ball.draw(screen)

        # Visual Score (using rectangles since font module is failing)
        # Player score: Green bars on the left
        for _ in range(player_score):
            pygame.draw.rect(screen, (0, 255, 0), (10, 10 + (_ * 20), 10, 10))
        # AI score: Red bars on the right
        for _ in range(ai_score):
            pygame.draw.rect(
                screen, (255, 0, 0), (SCREEN_WIDTH - 20, 10 + (_ * 20), 10, 10)
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
