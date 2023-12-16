import pygame
import random
import math

pygame.init()
pygame.display.set_caption('Pong')

width = 800
height = 500
screen = pygame.display.set_mode((width, height))

background_color = (0, 0, 0)

fps = 60
clock = pygame.time.Clock()

fonts = [pygame.font.SysFont("arial", font_size) for font_size in range(300)]


# Note that Sound and Settings are placed abnormally high in the main file
#    Once we start using multiple python files, we can make this cleaner using imports.


# Create directory resources, then add the music/sound files inside to make it work.

class Sound:
    def __init__(self, ball_bounce: str, score_point: str, score_point_volume: float, game_start: str, countdown: str,
                 game_over: str, music: str):
        self.ball_bounce = pygame.mixer.Sound(ball_bounce)
        self.score_point = pygame.mixer.Sound(score_point)

        self.score_point.set_volume(score_point_volume)

        self.game_start = pygame.mixer.Sound(game_start)
        self.countdown = pygame.mixer.Sound(countdown)
        self.game_over = pygame.mixer.Sound(game_over)

        self.music = music


sound = Sound(ball_bounce="resources/ball_bounce.wav", score_point="resources/score_point.wav", score_point_volume=0.1,
              game_start="resources/game_start.wav", countdown="resources/countdown.wav",
              game_over="resources/game_over.wav", music="resources/music.wav")

pygame.mixer.music.load(sound.music)


class Settings:
    def __init__(self, *, play_music, music_toggle_key, pause_key):
        self.play_music = play_music
        self.music_toggle_key = music_toggle_key
        self.pause_key = pause_key


settings = Settings(play_music=False, music_toggle_key=pygame.K_m, pause_key=pygame.K_SPACE)

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
    paddle_1 = Paddle(x=50, y=height / 2, acc=400, de_acc=800, paddle_width=5, paddle_height=60, max_speed=400,
                      up_key=pygame.K_w, down_key=pygame.K_s, color=(255, 100, 100))
    paddle_2 = Paddle(x=width - 50, y=height / 2, de_acc=800, acc=400, paddle_width=5, paddle_height=60, max_speed=400,
                      up_key=pygame.K_UP, down_key=pygame.K_DOWN, color=(100, 255, 100))

    collision_particle_system = ParticleSystem(acc=(0, 100), lifetime=1, speed=100, start_color=(255, 255, 255),
                                               end_color=(0, 0, 0), start_radius=2, end_radius=4, particle_count=20)

    trail_particle_system = ParticleSystem(lifetime=1, start_color=(255, 255, 255), end_color=(0, 0, 0),
                                           start_radius=5, end_radius=0, border_width=0)

    ball = Ball(x=width / 2, y=height / 2, radius=10, speed_x=200, color=(0, 255, 255),
                trail=trail_particle_system, collision=collision_particle_system)

    background_particle_system = ParticleSystem(lifetime=2, vel=(2, 0), start_color=(255, 255, 255),
                                                end_color=(0, 0, 0), start_radius=2, end_radius=4, particle_count=1)

    sound.game_start.play()
    if settings.play_music:
        pygame.mixer.music.play(loops=-1)

    while True:
        for event in pygame.event.get():
            quit_program_if_correct_key_pressed_or_screen_exit(event)
            end_music_if_key_pressed(event)
            pause_game_if_key_pressed(event)

        draw_background_game_loop()

        background_particle_system.create_background_particles()

        draw_scoreboard(paddle_1.score, paddle_2.score)

        background_particle_system.update(1 / fps)

        paddle_1.update(1 / fps)
        paddle_2.update(1 / fps)

        ball.update(1 / fps, paddle_left=paddle_1, paddle_right=paddle_2)

        if paddle_1.score >= score_required_to_win:
            pygame.mixer.stop()
            sound.game_over.play()
            ended_game_loop(score_required_to_win, 1)
        if paddle_2.score >= score_required_to_win:
            pygame.mixer.stop()
            sound.game_over.play()
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
        for event in pygame.event.get():
            quit_program_if_correct_key_pressed_or_screen_exit(event)
            end_music_if_key_pressed(event)

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
        for event in pygame.event.get():
            quit_program_if_correct_key_pressed_or_screen_exit(event)
            end_music_if_key_pressed(event)

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


def quit_program_if_correct_key_pressed_or_screen_exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        exit()


def end_music_if_key_pressed(event):
    if event.type == pygame.KEYDOWN and event.key == settings.music_toggle_key:
        settings.play_music = not settings.play_music

        if settings.play_music:
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.stop()


def pause_game_if_key_pressed(event):
    if event.type == pygame.KEYDOWN and event.key == settings.pause_key:
        draw_text_centered("Game Paused", width / 2, height / 2, "white", display_rect=False, font_size=45)
        pygame.display.update()
        game_paused_loop()


def game_paused_loop():
    while True:
        for event in pygame.event.get():
            quit_program_if_correct_key_pressed_or_screen_exit(event)
            end_music_if_key_pressed(event)
            if event.type == pygame.KEYDOWN and event.key == settings.pause_key:
                return


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


class Paddle:
    def __init__(self, *, x, y, paddle_width, paddle_height, speed, up_key, down_key,
                 color=(255, 255, 255), border_width=0):
        self.score = 0

        self.x = x
        self.y = y
        self.width = paddle_width
        self.height = paddle_height

        # Acceleration set, such that the paddle reaches [speed] speed after 1 second
        self.acc = speed * 2.60815358903 

        self.y_vel = 0

        self.up_key = up_key
        self.down_key = down_key

        self.color = color
        self.border_width = border_width

    def update(self, dt):
        self.move_on_input(dt)
        self.draw()
    
    def move_on_input(self, dt):
        keys = pygame.key.get_pressed()

        acc = 0
        if keys[self.up_key]:
            acc -= self.acc
        if keys[self.down_key]:
            acc += self.acc

        self.y_vel += acc * dt
        self.y_vel *= 0.08 ** dt

        self.y += self.y_vel * dt
        
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_low, self.y_low, self.width, self.height],
                         self.border_width)

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
    def __init__(self, *, x, y, radius, speed_x, color=(255, 255, 255), border_width=0, trail, collision, speedup=1.1):
        self.x = x
        self.y = y

        self.x_value_to_reset_to = x
        self.y_value_to_reset_to = y

        self.trail_particle_system: ParticleSystem = trail

        self.collision_particle_system: ParticleSystem = collision

        self.vy = random.uniform(speed_x / 3, speed_x * 2 / 3) * random.choice([-1, 1])
        self.vx = speed_x

        self.radius = radius
        self.speed_x = abs(speed_x)
        self.color = color
        self.border_width = border_width

        self.speedup = speedup

        self.time_elapsed = 0

    def update(self, dt, *, paddle_left, paddle_right):
        self.account_for_paddle_collision(paddle_left, paddle_right)

        self.account_for_vertical_screen_collision()

        self.account_score_increases(paddle_left, paddle_right)

        self.trail_particle_system.create_trail_particles(pos=(self.x + 2.5, self.y + 2.5))
        self.trail_particle_system.update(dt)

        self.collision_particle_system.update(dt)

        if self.time_elapsed >= 2.5: self.move(dt)
        self.time_elapsed += dt

        self.draw()

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.border_width)

    def account_for_paddle_collision(self, paddle_left: Paddle, paddle_right: Paddle) -> None:
        paddle_collided = None

        if self.does_collide(paddle_left):
            self.vx = abs(self.vx)
            paddle_collided = paddle_left
        if self.does_collide(paddle_right):
            self.vx = -abs(self.vx)
            paddle_collided = paddle_right

        if paddle_collided is not None:
            sound.ball_bounce.play()
            self.collision_particle_system.create_collision_particles(pos=(self.x, self.y))

    def account_for_vertical_screen_collision(self):
        if self.y_low < 0:
            self.y_low = 0
            self.vy = abs(self.vy)
            sound.ball_bounce.play()
            self.collision_particle_system.create_collision_particles(pos=(self.x, self.y))
        if self.y_high > height:
            self.y_high = height
            self.vy = -abs(self.vy)
            sound.ball_bounce.play()
            self.collision_particle_system.create_collision_particles(pos=(self.x, self.y))

    def account_score_increases(self, left_paddle: Paddle, right_paddle: Paddle):
        if self.x_low < 0:
            self.collision_particle_system.create_collision_particles(pos=(self.x, self.y))
            sound.score_point.play()
            right_paddle.score += 1
            self.reset()
        if self.x_high > width:
            self.collision_particle_system.create_collision_particles(pos=(self.x, self.y))
            sound.score_point.play()
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

        self.time_elapsed = 0
        sound.countdown.play()

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


class ParticleSystem:
    def __init__(self, *, lifetime, vel=(0, 0), start_color, end_color, start_radius, end_radius=0, border_width=0,
                 particle_count=0, acc=(0, 0), speed=0):
        self.particles = []
        self.lifetime = lifetime
        self.vel = vel
        self.start_color = start_color
        self.end_color = end_color
        self.start_radius = start_radius
        self.end_radius = end_radius
        self.border_width = border_width
        self.particle_count = particle_count
        self.acc = acc
        self.speed = speed

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        self.remove_dead_particles()

    def remove_dead_particles(self):
        alive_particles = []
        for particle in self.particles:
            if particle.is_alive():
                alive_particles.append(particle)
        self.particles = alive_particles

    def create_trail_particles(self, *, pos):
        self.particles.append(Particle(pos=pos, lifetime=self.lifetime, vel=self.vel, start_color=self.start_color,
                                       end_color=self.end_color,
                                       start_radius=self.start_radius, end_radius=self.end_radius,
                                       border_width=self.border_width))

    def create_collision_particles(self, *, pos):
        # Later on, we will create a menu system that you can add these particle settings to.

        for i in range(0, self.particle_count):
            # finds a random point on a circle around the point of collision
            angle = random.random() * math.tau
            random_vel = (math.cos(angle) * self.speed, math.sin(angle) * self.speed)

            self.particles.append(
                Particle(pos=pos, lifetime=self.lifetime, vel=random_vel, acc=self.acc, start_color=self.start_color,
                         end_color=self.end_color, start_radius=self.start_radius, end_radius=self.end_radius,
                         border_width=self.border_width))

    def create_background_particles(self):
        for i in range(0, self.particle_count):
            random_pos = (random.randint(0, width), random.randint(0, height))
            self.particles.append(
                Particle(pos=random_pos, lifetime=self.lifetime, vel=self.vel, start_color=self.start_color,
                         end_color=self.end_color,
                         start_radius=self.start_radius, end_radius=self.end_radius, border_width=self.border_width))


class Particle:
    def __init__(self, *, lifetime, pos, vel, acc=(0, 0), start_color, end_color, start_radius, end_radius=0,
                 border_width=0):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.acc = pygame.Vector2(acc)

        self.color = Color(start_color)
        self.color_change = (Color(end_color) - Color(start_color)) / lifetime

        self.radius = start_radius
        self.radius_change = (end_radius - start_radius) / lifetime

        self.border_width = border_width
        self.lifetime = lifetime

    def update(self, dt):
        self.move(dt)
        self.shrink(dt)
        self.fade(dt)
        self.draw()
        self.update_time(dt)

    def move(self, dt):
        self.pos += self.vel * dt
        self.vel += self.acc * dt

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius, self.border_width)

    def shrink(self, dt):
        self.radius += self.radius_change * dt
        if self.radius < 0:
            self.radius = 0

    def fade(self, dt):
        self.color += self.color_change * dt
        self.color.keep_within_bounds()

    def update_time(self, dt):
        self.lifetime -= dt

    def is_alive(self):
        return self.lifetime > 0


class Color:
    """
    We can change this to be easier once we use inheritance.
    """

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
        return Color(self.vec + Color(col).vec)

    def __sub__(self, col):
        return Color(self.vec - Color(col).vec)

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


menu_loop(score_required_to_win=2)
