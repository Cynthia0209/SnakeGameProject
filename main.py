import random
import sys

import pygame
from pygame.math import Vector2


class FRUIT:
    # construct a fruit in a random location
    def __init__(self):
        self.x = random.randint(5, int(cell_number * 1.5) - 5)
        self.y = random.randint(5, cell_number - 5)
        self.pos = Vector2(self.x, self.y)

    # draw the fruit in the given location
    def draw_fruit(self):
        fruit = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        new_apple = pygame.transform.scale(red_apple, (cell_size, cell_size))
        screen.blit(new_apple, fruit)

    # update the fruit after been eaten
    def update(self):
        self.x = random.randint(5, int(cell_number * 1.5) - 1)
        self.y = random.randint(5, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    # construct a snake in a random location
    def __init__(self, i, body_color_2, body_color_1, head_color):
        self.x = cell_number / 2
        self.y = cell_number / 2 - i
        self.body = [Vector2(self.x, self.y)]
        self.direction = Vector2(0, 0)
        self.eat = False
        self.score = 0
        self.head_color = head_color
        self.body_color_1 = body_color_1
        self.body_color_2 = body_color_2
        self.lose = 0

    # draw the snake in the given location
    def draw_snake(self):
        i = 0
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if i == 0:
                pygame.draw.rect(screen, self.head_color, block_rect)
            elif i % 2 == 0:
                pygame.draw.rect(screen, self.body_color_1, block_rect)
            else:
                pygame.draw.rect(screen, self.body_color_2, block_rect)
            i = i + 1

    # move snake by adding a new block before the original body.
    # Delete the last block if eat is False, True otherwise
    def move_snake(self):
        if self.eat:
            new_body = self.body
            self.score = self.score + 1
            new_body.insert(0, new_body[0] + self.direction)
        else:
            if len(self.body) == 1:
                new_body = [self.direction + self.body[0]]
            else:
                new_body = self.body[:-1]
                new_body.insert(0, new_body[0] + self.direction)

        self.body = new_body


# separate a sub screen showing scores
def draw_sub_screen(color):
    sub_screen = pygame.Rect(screen_size_x - 10 * cell_size, 0, 2, screen_size_y)
    pygame.draw.rect(screen, color, sub_screen)


# draw out the given score in the given color
def draw_score(score, number, color, s):
    game_font = pygame.font.Font("something_else/go3v2.ttf", 18)
    score_text = s + " " + ": " + str(score)
    score_surface = game_font.render(score_text, True, (0, 0, 0))
    score_x = screen_size_x - 6 * cell_size
    score_y = 10 + number * 2
    score_rec = score_surface.get_rect(center=(score_x, score_y))
    screen.blit(score_surface, score_rec)
    block = pygame.Rect(score_x - 3 * cell_size, score_y - 8, 18, 18)
    pygame.draw.rect(screen, color, block)


class SNAKEGAME:
    # construct a snake game with a snake and an apple
    def __init__(self):
        self.snake_one = SNAKE(0, (70, 130, 180), (175, 238, 238), (135, 206, 235))
        self.snake_two = SNAKE(10, (200, 50, 50), (255, 150, 150), (255, 0, 0))
        self.apple = FRUIT()
        self.round = 1
        self.time = 200
        self.max_score = 0
        self.begin = False

    # update the snake during each move
    def update(self):
        self.snake_one.move_snake()
        self.snake_two.move_snake()
        self.check_eat()
        self.check_fail()

    # draw the snakes and apple and the score
    def draw(self):
        self.snake_one.draw_snake()
        self.snake_two.draw_snake()
        self.apple.draw_fruit()
        draw_score(self.snake_one.score, 0, (135, 206, 235), "score")
        draw_score(self.snake_two.score, 20, (255, 0, 0), "score")
        draw_score(self.snake_one.lose, 10, (135, 206, 235), "lose")
        draw_score(self.snake_two.lose, 30, (255, 0, 0), "lose")
        self.draw_round()
        self.draw_max_score()
        self.draw_winner()

    # check whether the snake eat the apple
    def check_eat(self):
        if self.apple.pos == self.snake_one.body[0]:
            self.apple.update()
            self.snake_one.eat = True
            self.time = self.time - 5
            self.snake_one.move_snake()
            self.snake_one.eat = False
        for block in self.snake_one.body[1:]:
            if block == self.apple.pos:
                self.apple.update()

        if self.apple.pos == self.snake_two.body[0]:
            self.apple.update()
            self.snake_two.eat = True
            self.time = self.time - 8
            self.snake_two.move_snake()
            self.snake_two.eat = False
        for block in self.snake_two.body[1:]:
            if block == self.apple.pos:
                self.apple.update()

    # check whether the snake hit the wall or hit itself or hit each other
    def check_fail(self):
        if (len(self.snake_one.body) - 2) > self.max_score:
            self.max_score = (len(self.snake_one.body) - 1)

        if (len(self.snake_two.body) - 2) > self.max_score:
            self.max_score = (len(self.snake_two.body) - 1)

        if not (0 <= self.snake_one.body[0].x < cell_number * 1.5) or not (0 <= self.snake_one.body[0].y < cell_number):
            self.reset(self.snake_one)
            self.round = self.round + 1
            self.snake_one.lose = self.snake_one.lose + 1

        if not (0 <= self.snake_two.body[0].x < cell_number * 1.5) or not (0 <= self.snake_two.body[0].y < cell_number):
            self.reset(self.snake_two)
            self.round = self.round + 1
            self.snake_two.lose = self.snake_two.lose + 1

        for block in self.snake_one.body[1:]:
            if block == self.snake_two.body[0]:
                self.reset(self.snake_two)
                self.round = self.round + 1
                self.snake_two.lose = self.snake_two.lose + 1
            if block == self.snake_one.body[0]:
                self.reset(self.snake_one)
                self.round = self.round + 1
                self.snake_one.lose = self.snake_one.lose + 1

        for block in self.snake_two.body[1:]:
            if block == self.snake_two.body[0]:
                self.reset(self.snake_two)
                self.round = self.round + 1
                self.snake_two.lose = self.snake_two.lose + 1
            if block == self.snake_one.body[0]:
                self.reset(self.snake_one)
                self.round = self.round + 1
                self.snake_one.lose = self.snake_one.lose + 1

    # reset the given snake
    def reset(self, snake):
        x = random.randint(5, int(cell_number * 1.5) - 5)
        y = random.randint(5, cell_number - 5)
        snake.body = [Vector2(x, y)]
        snake.score = 0
        snake.direction = Vector2(0, 0)
        self.time = 200

    # draw the max score so far
    def draw_max_score(self):
        game_font = pygame.font.Font("something_else/go3v2.ttf", 18)
        score_text = "max score" + ": " + str(self.max_score)
        score_surface = game_font.render(score_text, True, (0, 0, 0))
        score_x = screen_size_x - 6 * cell_size - 15
        score_y = 120
        score_rec = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rec)

    # draw the number of rounds so dar
    def draw_round(self):
        game_font = pygame.font.Font("something_else/go3v2.ttf", 20)
        text = "round" + ": " + str(self.round)
        surface = game_font.render(text, True, (0, 0, 0))
        x = screen_size_x - 6 * cell_size - 15
        y = 180
        rec = surface.get_rect(center=(x, y))
        screen.blit(surface, rec)

    # get the winner
    def get_winner(self):
        if self.snake_one.lose == self.snake_two.lose:
            winner = "Tie"
        elif self.snake_one.lose > self.snake_two.lose:
            winner = "Red Snake"
        else:
            winner = "Blue Snake"
        return winner

    # draw the winner
    def draw_winner(self):
        winner = self.get_winner()
        game_font = pygame.font.Font("something_else/go3v2.ttf", 20)
        text = "winner" + ": " + winner
        surface = game_font.render(text, True, (0, 0, 0))
        x = screen_size_x - 6 * cell_size
        y = 300
        rec = surface.get_rect(center=(x, y))
        screen.blit(surface, rec)
        if winner == "Tie":
            draw_sub_screen((0, 0, 0))
        elif winner == "Red Snake":
            draw_sub_screen((200, 50, 50))
        else:
            draw_sub_screen((70, 130, 180))

    # initialize the snake game
    def main(self):
        screen_update = pygame.USEREVENT
        pygame.display.set_caption("snake game")
        pygame.time.set_timer(screen_update, self.time)
        screen.fill((255, 255, 255))

        while not self.begin:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pygame.display.update()
                    screen.fill((255, 255, 255))
                    self.draw()
                    pygame.display.update()
                    self.begin = True

        while True:
            self.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == screen_update:
                    self.update()
                    pygame.time.set_timer(screen_update, self.time)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.snake_one.direction.x != 1:
                            self.snake_one.direction = Vector2(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        if self.snake_one.direction.x != -1:
                            self.snake_one.direction = Vector2(1, 0)
                    elif event.key == pygame.K_UP:
                        if self.snake_one.direction.y != 1:
                            self.snake_one.direction = Vector2(0, -1)
                    elif event.key == pygame.K_DOWN:
                        if self.snake_one.direction.y != -1:
                            self.snake_one.direction = Vector2(0, 1)
                    elif event.key == pygame.K_a:
                        if self.snake_two.direction.x != 1:
                            self.snake_two.direction = Vector2(-1, 0)
                    elif event.key == pygame.K_d:
                        if self.snake_two.direction.x != -1:
                            self.snake_two.direction = Vector2(1, 0)
                    elif event.key == pygame.K_w:
                        if self.snake_two.direction.y != 1:
                            self.snake_two.direction = Vector2(0, -1)
                    elif event.key == pygame.K_s:
                        if self.snake_two.direction.y != -1:
                            self.snake_two.direction = Vector2(0, 1)

            screen.fill((255, 255, 255))
            self.draw()
            pygame.display.update()


cell_number = 32
cell_size = 24
screen_size_x = cell_size * cell_number * 1.5 + 10 * cell_size
screen_size_y = cell_size * cell_number
red = (255, 0, 0)
screen = pygame.display.set_mode((screen_size_x, screen_size_y))
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
text_x = screen_size_x / 2
text_y = screen_size_y / 2
screen.blit(text_surface, (text_x, text_y))
screen.blit(text_surface2, (text_x, text_y + 40))
font = pygame.font.SysFont("something_else/go3v2.ttf", 36)
pygame.display.update()
game = SNAKEGAME()
game.main()
