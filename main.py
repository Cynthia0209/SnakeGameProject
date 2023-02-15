import random
import sys

import pygame
from pygame.math import Vector2


class FRUIT:
    # construct a fruit in a random location
    def __init__(self):
        self.x = random.randint(5, cell_number - 5)
        self.y = random.randint(5, cell_number - 5)
        self.pos = Vector2(self.x, self.y)

    # draw the fruit in the given location
    def draw_fruit(self):
        fruit = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        new_apple = pygame.transform.scale(red_apple, (cell_size, cell_size))
        screen.blit(new_apple, fruit)

    def update(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    # construct a snake in a random location
    def __init__(self):
        self.x = cell_number / 2
        self.y = cell_number / 2
        self.body = [Vector2(self.x, self.y), Vector2(self.x + 1, self.y)]
        self.direction = Vector2(1, 0)
        self.eat = False

    # draw the snake in the given location
    def draw_snake(self):
        i = 0
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if i == 0:
                pygame.draw.rect(screen, head_color, block_rect)
            elif i % 2 == 0:
                pygame.draw.rect(screen, body_color_1, block_rect)
            else:
                pygame.draw.rect(screen, body_color_2, block_rect)
            i = i + 1

    # move snake by adding a new block before the original body.
    # Delete the last block if eat is False, True otherwise
    def move_snake(self):
        if self.eat:
            new_body = self.body[:]
        else:
            new_body = self.body[:-1]

        new_body.insert(0, new_body[0] + self.direction)
        self.body = new_body


class SNAKEGAME:
    # construct a snake game with a snake and an apple
    def __init__(self):
        self.snake = SNAKE()
        self.apple = FRUIT()
        self.attempt = 1
        self.time = 150
        self.max_score = 0

    # update the snake during each move
    def update(self):
        self.snake.move_snake()
        self.check_eat()
        self.check_fail()

    # draw the snake and the apple
    def draw(self):
        self.snake.draw_snake()
        self.apple.draw_fruit()
        self.draw_score()
        self.draw_attempt()
        self.draw_max_score()

    # check whether the snake eat the apple
    def check_eat(self):
        if self.apple.pos == self.snake.body[0]:
            self.apple.update()
            self.snake.eat = True
            self.snake.move_snake()
            self.snake.eat = False
        for block in self.snake.body[1:]:
            if block == self.apple.pos:
                self.apple.update()
                self.time = self.time - 10
                pygame.time.delay(self.time)

    # check whether the snake hit the wall or hit itself
    def check_fail(self):
        if (len(self.snake.body) - 2) > self.max_score:
            self.max_score = (len(self.snake.body) - 2)
        if not (0 <= self.snake.body[0].x < cell_number) or not (0 <= self.snake.body[0].y < cell_number):
            self.reset()
            self.attempt = self.attempt + 1

        for block in self.snake.body[2:]:
            if block == self.snake.body[0]:
                self.reset()
                self.attempt = self.attempt + 1

    # reset the game
    def reset(self):
        x = cell_number / 2
        y = cell_number / 2
        self.snake.body = [Vector2(x, y), Vector2(x + 1, y)]
        self.snake.direction = Vector2(0, 0)
        self.time = 100

    # draw the score
    def draw_score(self):
        game_font = pygame.font.Font("something_else/go3v2.ttf", 20)
        score_text = "score" + ": " + str(len(self.snake.body) - 2)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rec = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rec)

    def draw_max_score(self):
        game_font = pygame.font.Font("something_else/go3v2.ttf", 20)
        score_text = "max score" + ": " + str(self.max_score)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = 70
        score_y = (cell_size * cell_number - 40)
        score_rec = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rec)

    # draw the attempt
    def draw_attempt(self):
        game_font = pygame.font.Font("something_else/go3v2.ttf", 20)
        text = "attempt" + ": " + str(self.attempt)
        surface = game_font.render(text, True, (56, 74, 12))
        x = 60
        y = 40
        rec = surface.get_rect(center=(x, y))
        screen.blit(surface, rec)

    def main(self):
        screen_update = pygame.USEREVENT
        pygame.display.set_caption("snake game")
        pygame.time.set_timer(screen_update, 150)
        begin = False
        screen.fill((255, 255, 255))

        while not begin:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pygame.display.update()
                    screen.fill((255, 255, 255))
                    self.draw()
                    pygame.display.update()
                    begin = True

        while True:
            self.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == screen_update:
                    self.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.snake.direction.x != 1:
                            self.snake.direction = Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        if self.snake.direction.x != -1:
                            self.snake.direction = Vector2(1, 0)
                    elif event.key == pygame.K_UP:
                        if self.snake.direction.y != 1:
                            self.snake.direction = Vector2(0, -1)
                    elif event.key == pygame.K_DOWN:
                        if self.snake.direction.y != -1:
                            self.snake.direction = Vector2(0, 1)
            screen.fill((255, 255, 255))
            self.draw()
            pygame.display.update()


cell_number = 32
cell_size = 24
screen_size = cell_size * cell_number
body_color_2 = (70, 130, 180)
body_color_1 = (175, 238, 238)
head_color = (135, 206, 235)
red = (255, 0, 0)
screen = pygame.display.set_mode((screen_size, screen_size))
red_apple = pygame.image.load('something_else/red_apple.png').convert_alpha()

pygame.init()
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
screen.fill((255, 255, 255))
clock.tick(60)
font = pygame.font.SysFont("something_else/go3v2.ttf", 50)
font2 = pygame.font.SysFont("something_else/go3v2.ttf", 30)
text_surface = font.render("Welcome to Snake Game", True, (0, 0, 0))
text_surface2 = font2.render("Press any key to begin", True, (0, 0, 0))
display_info = pygame.display.Info()
text_x = display_info.current_w / 4
text_y = display_info.current_h / 4
screen.blit(text_surface, (text_x, text_y))
screen.blit(text_surface2, (text_x + 80, text_y + 50))
font = pygame.font.SysFont("something_else/go3v2.ttf", 36)
pygame.display.update()
game = SNAKEGAME()
game.main()
