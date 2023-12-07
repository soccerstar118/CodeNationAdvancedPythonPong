import pygame
import random

pygame.init()
pygame.display.set_caption('Game')

width = 800
height = 500
screen = pygame.display.set_mode((width, height))

background_color = (0, 0, 0)

fps = 60
clock = pygame.time.Clock()

font_size = 72
font = pygame.font.SysFont("arial", font_size)


def game_loop(score_required_to_win):
    paddle_1 = Paddle(x=50, y=height / 2, paddle_width=5, paddle_height=60, speed=400, up_key=pygame.K_w,
                      down_key=pygame.K_s, color=(255, 100, 100))
    paddle_2 = Paddle(x=width - 50, y=height / 2, paddle_width=5, paddle_height=60, speed=400, up_key=pygame.K_UP,
                      down_key=pygame.K_DOWN, color=(100, 255, 100))

    ball = Ball(x=width / 2, y=height / 2, radius=10, speed_x=400, color=(0, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.quit()
                quit()

        draw_background()
        draw_scoreboard(paddle_1.score, paddle_2.score)

        paddle_1.update(1 / fps)
        paddle_2.update(1 / fps)

        ball.update(1 / fps, paddle_left=paddle_1, paddle_right=paddle_2)

        if paddle_1.score >= score_required_to_win:
            print('Player 1 wins!')
            return
        if paddle_2.score >= score_required_to_win:
            print('Player 2 wins!')
            return

        pygame.display.update()
        clock.tick(fps)


def draw_scoreboard(score_1, score_2):
    # Set up text

    amount_offset_x = 50
    amount_offset_y = 50
    for (dx, score) in [(-amount_offset_x, score_1), (amount_offset_x, score_2)]:
        # Get text surface and rectangle
        text_surface = font.render(str(score), True, "white")
        text_rect = text_surface.get_rect(center=(width // 2 + dx, amount_offset_y))
        screen.blit(text_surface, text_rect)


def draw_background():
    screen.fill(background_color)

    # Drawing gray-dashes
    gray_color = (200, 200, 200)

    length_gray_dash = 50
    length_empty_space = 30

    width_dash = 5

    for y in range(0, width, length_empty_space + length_gray_dash):
        pygame.draw.rect(screen, gray_color, [width / 2 - width_dash / 2, y, width_dash, length_gray_dash])


class Paddle:
    def __init__(self, *, x, y, paddle_width, paddle_height, speed, up_key, down_key, color=(255, 255, 255),
                 border_width=0):
        self.score = 0

        self.x = x
        self.y = y
        self.width = paddle_width
        self.height = paddle_height

        self.speed = abs(speed)

        self.up_key = up_key
        self.down_key = down_key

        self.color = color
        self.border_width = border_width

    def update(self, dt):
        self.move_on_input(dt)
        self.draw()

    def move_on_input(self, dt):
        keys = pygame.key.get_pressed()

        incr_amount = 0
        if keys[self.up_key]:
            incr_amount -= self.speed
        if keys[self.down_key]:
            incr_amount += self.speed

        self.y += incr_amount * dt

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.get_x_low(), self.get_y_low(), self.width, self.height],
                         self.border_width)

    def get_points(self):
        return [(self.get_x_low(), self.get_y_low()),
                (self.get_x_low(), self.get_y_high()),
                (self.get_x_high(), self.get_y_high()),
                (self.get_x_high(), self.get_y_low())]

    # Later on, we will learn the Pythonic way to do it, but for now we will use more Java-style ones.

    def get_x_low(self):
        return self.x - self.width / 2

    def get_x_high(self):
        return self.x + self.width / 2

    def get_y_low(self):
        return self.y - self.height / 2

    def get_y_high(self):
        return self.y + self.height / 2


class Ball:
    def __init__(self, *, x, y, radius, speed_x, color=(255, 255, 255), border_width=0):
        self.x = x
        self.y = y

        self.x_value_to_reset_to = x
        self.y_value_to_reset_to = y

        self.vy = random.uniform(speed_x / 3, speed_x * 2 / 3) * random.choice([-1, 1])
        self.vx = speed_x

        self.radius = radius
        self.speed_x = abs(speed_x)
        self.color = color
        self.border_width = border_width

    def update(self, dt, *, paddle_left, paddle_right):
        self.account_for_paddle_collision(paddle_left)
        self.account_for_paddle_collision(paddle_right)

        self.account_for_vertical_screen_collision()

        self.account_score_increases(paddle_left, paddle_right)

        self.move(dt)
        self.draw()

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.border_width)

    def account_for_paddle_collision(self, paddle: Paddle) -> None:
        """
        Assumes the ball is relatively slow (i.e. won't clip through)
        Also does not use i-frames (i.e. collision could occur multiple times for a collision)
        Simply negates ball
        """

        if not self.does_collide(paddle):
            return

        self.vx = -self.vx

    def account_for_vertical_screen_collision(self):
        if self.get_y_low() < 0:
            self.set_y_low(0)
            self.vy = abs(self.vy)
        if self.get_y_high() > height:
            self.set_y_high(height)
            self.vy = -abs(self.vy)

    def account_score_increases(self, left_paddle: Paddle, right_paddle: Paddle):
        if self.get_x_low() < 0:
            right_paddle.score += 1
            self.reset_ball()
        if self.get_x_high() > width:
            left_paddle.score += 1
            self.reset_ball()

    def reset_ball(self):
        """
        Flips ball direction, resets position of ball.
        """

        self.vx = -self.vx
        self.vy = random.uniform(self.speed_x / 3, self.speed_x * 2 / 3) * random.choice([-1, 1])

        self.x = self.x_value_to_reset_to
        self.y = self.y_value_to_reset_to

    def does_collide(self, paddle):
        for point in self.get_points():
            if paddle.get_x_low() < point[0] < paddle.get_x_high() and paddle.get_y_low() < point[1] < \
                    paddle.get_y_high():
                return True
        return False

    def get_points(self):
        # This does make things scuffed, as circle is essentially treated as a square

        return [(self.get_x_low(), self.get_y_low()),
                (self.get_x_low(), self.get_y_high()),
                (self.get_x_high(), self.get_y_high()),
                (self.get_x_high(), self.get_y_low())]

    # Later on, we will learn the Pythonic way to do it, but for now we will use more Java-style ones.

    def get_x_low(self):
        return self.x - self.radius

    def get_x_high(self):
        return self.x + self.radius

    def get_y_low(self):
        return self.y - self.radius

    def get_y_high(self):
        return self.y + self.radius

    def set_x_low(self, num):
        self.x = num + self.radius

    def set_x_high(self, num):
        self.x = num - self.radius

    def set_y_low(self, num):
        self.y = num + self.radius

    def set_y_high(self, num):
        self.y = num - self.radius


game_loop(5)
