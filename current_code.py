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

fonts = [pygame.font.SysFont("arial", font_size) for font_size in range(300)]

'''
------------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------------
Later on, we will move to a class based menu system. For now we opt for functions for simplicity. 
------------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------------
'''


def game_loop(score_required_to_win):
    paddle_1 = Paddle(x=50, y=height / 2, paddle_width=5, paddle_height=60, speed=400, up_key=pygame.K_w,
                      down_key=pygame.K_s, color=(255, 100, 100))
    paddle_2 = Paddle(x=width - 50, y=height / 2, paddle_width=5, paddle_height=60, speed=400, up_key=pygame.K_UP,
                      down_key=pygame.K_DOWN, color=(100, 255, 100))

    ball = Ball(x=width / 2, y=height / 2, radius=10, speed_x=200, color=(0, 255, 255))
    while True:
        quit_program_if_correct_key_pressed_or_screen_exit()

        draw_background_game_loop()
        draw_scoreboard(paddle_1.score, paddle_2.score)

        paddle_1.update(1 / fps)
        paddle_2.update(1 / fps)

        ball.update(1 / fps, paddle_left=paddle_1, paddle_right=paddle_2)

        if paddle_1.score >= score_required_to_win:
            ended_game_loop(score_required_to_win, 1)
        if paddle_2.score >= score_required_to_win:
            ended_game_loop(score_required_to_win, 2)

        pygame.display.update()
        clock.tick(fps)


def draw_scoreboard(score_1, score_2):
    amount_offset_x = 50
    amount_offset_y = 50
    for (dx, score) in [(-amount_offset_x, score_1), (amount_offset_x, score_2)]:
        draw_text_centered(score, width // 2 + dx, amount_offset_y, "white")


def draw_background_game_loop():
    screen.fill(background_color)

    # Drawing gray-dashes
    gray_color = (200, 200, 200)

    length_gray_dash = 50
    length_empty_space = 30

    width_dash = 5

    for y in range(0, width, length_empty_space + length_gray_dash):
        pygame.draw.rect(screen, gray_color, [width / 2 - width_dash / 2, y, width_dash, length_gray_dash])


def ended_game_loop(score_required_to_win, num_player_won):
    while True:
        quit_program_if_correct_key_pressed_or_screen_exit()
        screen.fill(background_color)

        draw_text_centered(f"Player {num_player_won} wins! ", width / 2, height * 1 / 4, "white", display_rect=True,
                           rect_color="blue",
                           rect_border_width=5, rect_dx=50, rect_dy=50)

        draw_text_centered(" Press [Space] to start", width / 2, height * 2 / 4, "white", display_rect=True,
                           rect_color="red", rect_border_width=5, rect_dx=5, rect_dy=5, font_size=45)

        draw_text_centered(" Press [ESC] to end game", width / 2, height * 3 / 4, "white", display_rect=True,
                           rect_color="red", rect_border_width=5, rect_dx=5, rect_dy=5, font_size=45)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            game_loop(score_required_to_win)

        pygame.display.update()
        clock.tick(fps)


def menu_loop(score_required_to_win):
    while True:
        quit_program_if_correct_key_pressed_or_screen_exit()
        screen.fill(background_color)

        draw_text_centered("--- P O N G ---", width / 2, height / 2, "white", display_rect=True, rect_color="blue",
                           rect_border_width=5, rect_dx=50, rect_dy=50)

        draw_text_centered(" Press [Space] to start", width / 2, height * 3 / 4, "white", display_rect=True,
                           rect_color="red", rect_border_width=5, rect_dx=5, rect_dy=5, font_size=45)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            game_loop(score_required_to_win)

        pygame.display.update()
        clock.tick(fps)


def draw_text_centered(message, x, y, color="white", *, display_rect=False, rect_color: str | tuple = None,
                       rect_border_width=0, rect_dx=0, rect_dy=0, font_size=72):
    text_surface = fonts[font_size].render(str(message), True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    if display_rect:
        # If checks to avoid copying rectangle if not needed, as copying a rectangle can be slow.
        if not (rect_dx == 0 and rect_dy == 0):
            copied_rect = text_rect.copy()

            cx, cy = text_rect.center

            copied_rect.width = 2 * rect_dx + text_rect.width
            copied_rect.height = 2 * rect_dy + text_rect.height

            copied_rect.center = (cx, cy)

            pygame.draw.rect(screen, rect_color, copied_rect, rect_border_width)
        else:
            pygame.draw.rect(screen, rect_color, text_rect, rect_border_width)

    screen.blit(text_surface, text_rect)


def quit_program_if_correct_key_pressed_or_screen_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()


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
        pygame.draw.rect(screen, self.color, [self.x_low, self.y_low, self.width, self.height],
                         self.border_width)

    # Later on, we will learn the Pythonic way to do it, but for now we will use more Java-style ones.

    @property
    def x_low(self):
        return self.x - self.width / 2

    @x_low.setter
    def x_low(self, num):
        self.x = self.width / 2 + num

    @property
    def x_high(self):
        return self.x + self.width / 2

    @x_high.setter
    def x_high(self, num):
        self.x = -self.width / 2 + num

    @property
    def y_low(self):
        return self.y - self.height / 2

    @y_low.setter
    def y_low(self, num):
        self.y = self.height / 2 + num

    @property
    def y_high(self):
        return self.y + self.height / 2

    @y_high.setter
    def y_high(self, num):
        self.y = -self.height / 2 + num

    @property
    def left(self):
        return self.x_low

    @left.setter
    def left(self, num):
        self.x_low = num

    @property
    def right(self):
        return self.x_high

    @right.setter
    def right(self, num):
        self.x_high = num

    @property
    def top(self):
        return self.y_low

    @top.setter
    def top(self, num):
        self.y_low = num

    @property
    def bottom(self):
        return self.y_high

    @bottom.setter
    def bottom(self, num):
        self.y_high = num


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
        self.account_for_paddle_collision(paddle_left, paddle_right)

        self.account_for_vertical_screen_collision()

        self.account_score_increases(paddle_left, paddle_right)

        self.move(dt)
        self.draw()

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.border_width)

    def account_for_paddle_collision(self, paddle_left: Paddle, paddle_right: Paddle) -> None:
        """
        Assumes the ball is relatively slow (i.e. won't clip through)
        Also does not use i-frames (i.e. collision could occur multiple times for a collision)
        Simply negates ball
        """

        if self.does_collide(paddle_left):
            self.left = paddle_left.right
            self.vx = abs(self.vx)
        if self.does_collide(paddle_right):
            self.right = paddle_right.left
            self.vx = -abs(self.vx)

    def account_for_vertical_screen_collision(self):
        if self.y_low < 0:
            self.y_low = 0
            self.vy = abs(self.vy)
        if self.y_high > height:
            self.y_high = height
            self.vy = -abs(self.vy)

    def account_score_increases(self, left_paddle: Paddle, right_paddle: Paddle):
        if self.x_low < 0:
            right_paddle.score += 1
            self.reset()
        if self.x_high > width:
            left_paddle.score += 1
            self.reset()

    def reset(self):
        """
        Flips ball direction, resets position of ball.
        """

        self.vx = -self.vx
        self.vy = random.uniform(self.speed_x / 3, self.speed_x * 2 / 3) * random.choice([-1, 1])

        self.x = self.x_value_to_reset_to
        self.y = self.y_value_to_reset_to

    def does_collide(self, paddle):
        for point in self.get_points():
            if paddle.x_low < point[0] < paddle.x_high and paddle.y_low < point[1] < \
                    paddle.y_high:
                return True
        return False

    def get_points(self):
        # This does make things scuffed, as circle is essentially treated as a square

        return [(self.x_low, self.y_low),
                (self.x_low, self.y_high),
                (self.x_high, self.y_high),
                (self.x_high, self.y_low)]

    # Later on, we will learn the Pythonic way to do it, but for now we will use more Java-style ones.

    @property
    def x_low(self):
        return self.x - self.radius

    @x_low.setter
    def x_low(self, num):
        self.x = num + self.radius

    @property
    def x_high(self):
        return self.x + self.radius

    @x_high.setter
    def x_high(self, num):
        self.x = num - self.radius

    @property
    def y_low(self):
        return self.y - self.radius

    @y_low.setter
    def y_low(self, num):
        self.y = num + self.radius

    @property
    def y_high(self):
        return self.y + self.radius

    @y_high.setter
    def y_high(self, num):
        self.y = num - self.radius

    @property
    def left(self):
        return self.x_low

    @left.setter
    def left(self, num):
        self.x_low = num

    @property
    def right(self):
        return self.x_high

    @right.setter
    def right(self, num):
        self.x_high = num

    @property
    def top(self):
        return self.y_low

    @top.setter
    def top(self, num):
        self.y_low = num

    @property
    def bottom(self):
        return self.y_high

    @bottom.setter
    def bottom(self, num):
        self.y_high = num


class BackgroundParticleSystem:
    ...

class Particle:
    def __init__(self, *, lifetime, pos, vel, start_color, end_color, start_radius, end_radius=0, border_width=0):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)

        self.color = Color(start_color)
        self.color_change = (Color(end_color) - Color(start_color)) / lifetime

        self.radius = start_radius
        self.radius_change = (start_radius - end_radius) / lifetime

        self.border_width = border_width

    def update(self, dt):
        self.move(dt)
        self.shrink(dt)
        self.fade(dt)
        self.draw()

    def move(self, dt):
        self.pos += self.vel * dt

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius, self.border_width)

    def shrink(self, dt):
        self.radius += self.radius_change * dt
        if self.radius < 0:
            self.radius = 0

    def fade(self, dt):
        self.color += self.color_change * dt
        self.color.keep_within_bounds()


class Color:
    """
    We can change this to be easier once we use inheritance.
    """
    #the Particle class needs a method to check if alive (keep a variable equal to time alive, and decrease by dt upon update call) btw so add that
    #the Particle class needs a method to check if alive (keep a variable equal to time alive, and decrease by dt upon update call) btw so add that
    #the Particle class needs a method to check if alive (keep a variable equal to time alive, and decrease by dt upon update call) btw so add that
    #the Particle class needs a method to check if alive (keep a variable equal to time alive, and decrease by dt upon update call) btw so add that
    #the Particle class needs a method to check if alive (keep a variable equal to time alive, and decrease by dt upon update call) btw so add that
    #the Particle class needs a method to check if alive (keep a variable equal to time alive, and decrease by dt upon update call) btw so add that

    def __init__(self, col):
        self.vec = pygame.Vector3(col)

    def keep_within_bounds(self):
        for i in range(3):
            if self[i] < 0:
                self[i] = 0
            if self[i] > 255:
                self[i] = 255

    def __iter__(self):
        for i in range(3):
            yield self[i]

    def __getitem__(self, item):
        return self.vec[item]

    def __setitem__(self, key, value):
        self.vec[key] = value

    def __mul__(self, num):
        return Color(self.vec * num)

    def __add__(self, col):
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Change to Color(col).vec to be better (not changing rn since dont have time to test it)
        # Also for __sub__
        return Color(self.vec + pygame.Vector3(col))

    def __sub__(self, col):
        return Color(self.vec - pygame.Vector3(col))

    def __truediv__(self, num):
        return self * (1 / num)

    def __neg__(self):
        return self * -1

    def __len__(self):
        return 3

    def __str__(self):
        return f'Color({self.r}, {self.g}, {self.b})'

    @property
    def r(self):
        return self.vec[0]

    @r.setter
    def r(self, num):
        self.vec[0] = num

    @property
    def g(self):
        return self.vec[1]

    @g.setter
    def g(self, num):
        self.vec[1] = num

    @property
    def b(self):
        return self.vec[2]

    @b.setter
    def b(self, num):
        self.vec[2] = num

# menu_loop(5)
#
# x = Color(5, 5, 5)
# y = Color(4, 4, 4)
# print(- y / 5)
