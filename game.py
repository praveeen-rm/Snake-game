import pygame, sys, random
from pygame.math import Vector2
from os import path

# Game settings
TITLE = "Snake"
CELL_SIZE = 30
CELL_NUMBER = 20    
WIDTH = CELL_SIZE * CELL_NUMBER
HEIGHT = CELL_SIZE * CELL_NUMBER
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GREEN = (175, 215, 70)
DARK_GREEN = (167,209,61)

# Pygame Initializations
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Folders
game_folder = path.dirname(__file__)
assets_folder = path.join(game_folder, "assets")
fonts_folder = path.join(assets_folder, "fonts")
sounds_folder = path.join(assets_folder, "sounds")
sprites_folder = path.join(assets_folder, "sprites")
apple_folder = path.join(sprites_folder, "apple")
snake_folder = path.join(sprites_folder, "snake")
banner_folder = path.join(sprites_folder, "banner")

# Image Files
apple_img_file = path.join(apple_folder, "apple.png")

head_right_img_file = path.join(snake_folder, "head_right.png")
head_left_img_file = path.join(snake_folder, "head_left.png")
head_up_img_file = path.join(snake_folder, "head_up.png")
head_down_img_file = path.join(snake_folder, "head_down.png")

tail_right_img_file = path.join(snake_folder, "tail_right.png")
tail_left_img_file = path.join(snake_folder, "tail_left.png")
tail_up_img_file = path.join(snake_folder, "tail_up.png")
tail_down_img_file = path.join(snake_folder, "tail_down.png")

body_h_img_file = path.join(snake_folder, "body_horizontal.png")
body_v_img_file = path.join(snake_folder, "body_vertical.png")

body_tr_img_file = path.join(snake_folder, "body_tr.png")
body_tl_img_file = path.join(snake_folder, "body_tl.png")
body_br_img_file = path.join(snake_folder, "body_br.png")
body_bl_img_file = path.join(snake_folder, "body_bl.png")

game_over_img_file = path.join(banner_folder, "gameover.png")
start_img_file = path.join(banner_folder, "start_btn.png")
exit_img_file = path.join(banner_folder, "exit_btn.png")

# Other
font_name = path.join(fonts_folder, "04B_19.TTF")
hit_snd_file = path.join(sounds_folder, "hit.wav")
eat_snd_file = path.join(sounds_folder, "eat.wav")
bg_snd_file = path.join(sounds_folder, "happy.ogg")

hit_sound = pygame.mixer.Sound(hit_snd_file)
eat_sound = pygame.mixer.Sound(eat_snd_file)
bg_music = pygame.mixer.Sound(bg_snd_file)
bg_music.set_volume(1)

class Snake:
    def __init__(self):
        self.body = [Vector2(11, 10), Vector2(10, 10), Vector2(9, 10)]
        self.direction = Vector2(1, 0)
        self.new_body = False
        self.load_images()

    def load_images(self):
        self.head_right = pygame.image.load(head_right_img_file).convert_alpha()
        self.head_left = pygame.image.load(head_left_img_file).convert_alpha()
        self.head_up = pygame.image.load(head_up_img_file).convert_alpha()
        self.head_down = pygame.image.load(head_down_img_file).convert_alpha()

        self.tail_right = pygame.image.load(tail_right_img_file).convert_alpha()
        self.tail_left = pygame.image.load(tail_left_img_file).convert_alpha()
        self.tail_up = pygame.image.load(tail_up_img_file).convert_alpha()
        self.tail_down = pygame.image.load(tail_down_img_file).convert_alpha()

        self.body_horizontal = pygame.image.load(body_h_img_file).convert_alpha()
        self.body_vertical = pygame.image.load(body_v_img_file).convert_alpha()

        self.body_tr = pygame.image.load(body_tr_img_file).convert_alpha()
        self.body_tl = pygame.image.load(body_tl_img_file).convert_alpha()
        self.body_br = pygame.image.load(body_br_img_file).convert_alpha()
        self.body_bl = pygame.image.load(body_bl_img_file).convert_alpha()

        self.transform_images()

    def transform_images(self):
        self.head_right = pygame.transform.scale(self.head_right, (CELL_SIZE, CELL_SIZE))
        self.head_left = pygame.transform.scale(self.head_left, (CELL_SIZE, CELL_SIZE))
        self.head_up = pygame.transform.scale(self.head_up, (CELL_SIZE, CELL_SIZE))
        self.head_down = pygame.transform.scale(self.head_down, (CELL_SIZE, CELL_SIZE))

        self.tail_right = pygame.transform.scale(self.tail_right, (CELL_SIZE, CELL_SIZE))
        self.tail_left = pygame.transform.scale(self.tail_left, (CELL_SIZE, CELL_SIZE))
        self.tail_up = pygame.transform.scale(self.tail_up, (CELL_SIZE, CELL_SIZE))
        self.tail_down = pygame.transform.scale(self.tail_down, (CELL_SIZE, CELL_SIZE))

        self.body_horizontal = pygame.transform.scale(self.body_horizontal, (CELL_SIZE, CELL_SIZE))
        self.body_vertical = pygame.transform.scale(self.body_vertical, (CELL_SIZE, CELL_SIZE))

        self.body_tr = pygame.transform.scale(self.body_tr, (CELL_SIZE, CELL_SIZE))
        self.body_tl = pygame.transform.scale(self.body_tl, (CELL_SIZE, CELL_SIZE))
        self.body_br = pygame.transform.scale(self.body_br, (CELL_SIZE, CELL_SIZE))
        self.body_bl = pygame.transform.scale(self.body_bl, (CELL_SIZE, CELL_SIZE))


    def draw_snake(self):

        self.update_head_sprites()
        self.update_tail_sprites()

        for index, body in enumerate(self.body):
            body_x_pos = int(body.x*CELL_SIZE)
            body_y_pos = int(body.y*CELL_SIZE)
            self.body_rect = pygame.Rect(body_x_pos, body_y_pos, CELL_SIZE, CELL_SIZE)
            
            if index == 0: # Head
                screen.blit(self.head, self.body_rect)
            elif index == len(self.body) - 1: # Tail
                screen.blit(self.tail, self.body_rect)
            else:
                prev_body = self.body[index + 1] - body
                next_body = self.body[index - 1] - body
                if prev_body.x == next_body.x:
                    screen.blit(self.body_vertical, self.body_rect)
                elif prev_body.y == next_body.y:
                    screen.blit(self.body_horizontal, self.body_rect)
                else:
                    if prev_body.x == -1 and next_body.y == -1 or prev_body.y == -1 and next_body.x == -1:
                        screen.blit(self.body_tl, self.body_rect)
                    elif prev_body.x == -1 and next_body.y == 1 or prev_body.y == 1 and next_body.x == -1:
                        screen.blit(self.body_bl, self.body_rect)
                    elif prev_body.x == 1 and next_body.y == -1 or prev_body.y == -1 and next_body.x == 1:
                        screen.blit(self.body_tr, self.body_rect)
                    elif prev_body.x == 1 and next_body.y == 1 or prev_body.y == 1 and next_body.x == 1:
                        screen.blit(self.body_br, self.body_rect)

                # else:
                #     pygame.draw.rect(screen, BLUE, self.body_rect)

        # for b in self.body:
        #     b_x_pos = int(b.x*CELL_SIZE)
        #     b_y_pos = int(b.y*CELL_SIZE)
        #     b_rect = pygame.Rect(b_x_pos, b_y_pos, CELL_SIZE, CELL_SIZE)
        #     pygame.draw.rect(screen, BLUE, b_rect)

    def update_head_sprites(self):
        head_difference = self.body[1] - self.body[0]
        if head_difference == Vector2(1, 0): self.head = self.head_left
        elif head_difference == Vector2(-1, 0): self.head = self.head_right
        elif head_difference == Vector2(0, 1): self.head = self.head_up
        else: self.head = self.head_down

    def update_tail_sprites(self):
        l = len(self.body)
        tail_difference = self.body[l - 2] - self.body[l - 1]
        if tail_difference == Vector2(1, 0): self.tail = self.tail_left
        elif tail_difference == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_difference == Vector2(0, 1): self.tail = self.tail_up
        else: self.tail = self.tail_down

    def move_snake(self):
        if self.new_body:
            self.body_copy = self.body[:]
            self.body_copy.insert(0, self.body_copy[0] + self.direction)
            self.body = self.body_copy[:]
            self.new_body = False
        else:
            self.body_copy = self.body[:-1]
            self.body_copy.insert(0, self.body_copy[0] + self.direction)
            self.body = self.body_copy[:]

    def add_body(self):
        self.new_body = True

class Fruit:
    def __init__(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
        self.load_images()

    def load_images(self):
        self.fruit_img = pygame.image.load(apple_img_file).convert_alpha()
        self.fruit_img = pygame.transform.scale(self.fruit_img, (CELL_SIZE, CELL_SIZE))

    def draw_fruit(self):
        self.fruit_rect = pygame.Rect(int(self.pos.x*CELL_SIZE), int(self.pos.y*CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(self.fruit_img, self.fruit_rect)
        # pygame.draw.rect(screen, RED, self.fruit_rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self):
        bg_music.play(-1)
        self.playing = False
        self.start_screen = True
        self.game_start_screen()

    def new_game(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0
        self.playing = True
        self.start_screen = False

    def draw(self):
        self.draw_grass()
        if self.playing:
            self.draw_text(f"Score: {self.score}", 24, WHITE, WIDTH/2, 10)
            self.snake.draw_snake()
            self.fruit.draw_fruit()
        elif self.start_screen:
            self.game_start_screen()

    def draw_grass(self):
        for row in range(CELL_NUMBER):
            if row % 2 == 0:
                for col in range(CELL_NUMBER):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(row*CELL_SIZE, col*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, DARK_GREEN, grass_rect)
            else:
                for col in range(CELL_NUMBER):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(row*CELL_SIZE, col*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(screen, DARK_GREEN, grass_rect)
                

    def update(self):
        if self.playing:
            self.snake.move_snake()
            self.check_if_snake_eats_fruit()
            self.check_if_snake_hits_wall()
            self.check_if_snake_hits_itself()

    def check_if_snake_eats_fruit(self):
        if self.snake.body[0] == self.fruit.pos:
            self.score += 1
            eat_sound.play()
            self.fruit.randomize()
            self.snake.add_body()

    def check_if_snake_hits_wall(self):
        snake_head = self.snake.body[0]
        if snake_head.x > CELL_NUMBER-1 or snake_head.x < 0 or snake_head.y > CELL_NUMBER-1 or snake_head.y < 0:
            hit_sound.play()
            self.playing = False
            
    def check_if_snake_hits_itself(self):
        snake_head = self.snake.body[0]
        for body in self.snake.body[1:]:
            if body == snake_head:
                hit_sound.play()
                self.playing = False

    def game_over_screen(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.game_over_img = pygame.image.load(game_over_img_file).convert_alpha()
        self.game_over_img_rect = self.game_over_img.get_rect(center=(WIDTH/2, HEIGHT/4))
        screen.blit(self.game_over_img, self.game_over_img_rect)
        self.draw_text('Press "p" to try again', 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(f'SCORE: {self.score}', 34, WHITE, WIDTH/2, HEIGHT/2)
        pygame.display.update()
        self.wait_for_key()

    def game_start_screen(self):
        self.start_img = pygame.transform.scale(pygame.image.load(start_img_file).convert_alpha(),(100, 50))
        self.start_img_rect = self.start_img.get_rect()
        self.start_img_rect.left = 200
        self.start_img_rect.y = 100
        self.exit_img = pygame.transform.scale(pygame.image.load(exit_img_file).convert_alpha(),(100, 50))
        self.exit_img_rect = self.start_img.get_rect()
        self.exit_img_rect.right = WIDTH-200
        self.exit_img_rect.y = 100

        pos = pygame.mouse.get_pos()
        if self.start_img_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.new_game()
        if self.exit_img_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                running = False

        self.snake_img = pygame.transform.scale(pygame.image.load(head_up_img_file).convert_alpha(),(50, 50))
        self.snake_img_rect = self.snake_img.get_rect(center=(WIDTH/2, HEIGHT/2 + 100))

        screen.blit(self.start_img, self.start_img_rect)
        screen.blit(self.exit_img, self.exit_img_rect)
        screen.blit(self.snake_img, self.snake_img_rect)

        self.draw_text('OR', 25, WHITE, WIDTH/2, 200)
        self.draw_text('Press "s" to Start', 25, WHITE, WIDTH/2, 250)
        self.wait_for_key()

    def wait_for_key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.new_game()
                if event.key == pygame.K_s:
                    self.new_game()


    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)


main = Main()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Variables
running = True

while running:

    # clock/fps - frames per second 
    clock.tick(FPS)

    # input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SCREEN_UPDATE and main.playing:
            main.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main.snake.direction.y != 1:
                main.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main.snake.direction.y != -1:
                main.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main.snake.direction.x != 1:
                main.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main.snake.direction.x != -1:
                main.snake.direction = Vector2(1, 0)


    # draw/render
    screen.fill(LIGHT_GREEN)

    main.draw()

    if not main.playing and not main.start_screen:
        main.game_over_screen()


    # update/flip
    pygame.display.update()

bg_music.stop()
pygame.quit()
sys.exit()
