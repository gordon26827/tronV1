import pygame
from random import randint

bike_n = pygame.image.load("bike_n.png")
bike_s = pygame.image.load("bike_s.png")
bike_e = pygame.image.load("bike_e.png")
bike_w = pygame.image.load("bike_w.png")

width = 983
height = 598

players = [(217, 155, 0), (42, 42, 247), (109, 41, 255), (240, 240, 240)]
directions = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
bikes = {'N': bike_n, 'S': bike_s, 'E': bike_e, 'W': bike_w}
spawn_points = [[20, 20], [width - 20, 20], [20, height - 20], [width - 20, height - 20]]
spawn_directions = ['E', 'W', 'E', 'W']

class Node:
    def __init__(self, x, y):
        self.status = None
        self.x = x
        self.y = y
        self.width = 20


class Rider:
    instances = []

    def __init__(self, player_num):
        self.__class__.instances.append(self)
        self.id = player_num
        self.color = players[player_num]
        self.lines = [[spawn_points[player_num], spawn_points[player_num]]]
        self.recent = [spawn_points[player_num], spawn_points[player_num]]
        self.direction = spawn_directions[player_num]
        self.desired_length = 0
        self.length = 0
        self.is_alive = True
        self.velocity = 5

    def move(self, new_direction, players):
        if self.is_alive:
            new = directions[new_direction]
            prev = self.lines[-1][1]
            x, y = prev[0] + (new[0] * self.velocity), prev[1] + (new[1] * self.velocity)

            if self.direction == new_direction:
                self.lines[-1][1] = [x, y]

            else:
                self.direction = new_direction
                self.lines.append([prev, [x, y]])
                self.recent = self.lines[-1]

            if not 0 <= x <= width:
                sign = 1 if x < 0 else -1
                self.lines.append([[x + (width + 1) * sign, y], [x + (width + 1) * sign, y]])
                self.recent = self.lines[-1]
            elif not 0 <= y <= height:
                sign = 1 if y < 0 else -1
                self.lines.append([[x, y + (height + 1) * sign], [x, y + (height + 1) * sign]])
                self.recent = self.lines[-1]

            self.collision_detection(players)

            if self.desired_length:
                self.shorten()

    def collision_detection(self, players):
        recent = [self.recent[1], self.lines[-1][1]]
        recent_is_vertical = recent[0][0] == recent[1][0]
        if recent_is_vertical:
            for player in players:
                lines = player.lines[:-2] if player.id == self.id else player.lines
                for line in lines:
                    line_is_horizontal = line[0][1] == line[1][1]
                    if line_is_horizontal:
                        lines_intersect_x = line[0][0] <= recent[0][0] <= line[1][0] or line[1][0] <= recent[0][0] <= line[0][0]
                        lines_intersect_y = recent[0][1] <= line[0][1] <= recent[1][1] or recent[1][1] <= line[0][1] <= recent[0][1]
                        if lines_intersect_x and lines_intersect_y:
                            self.kill()
                            return
                    else:
                        lines_intersect_x = line[0][0] == recent[0][0]
                        lines_intersect_y = line[0][1] <= recent[1][1] <= line[1][1] or line[1][1] <= recent[1][1] <= line[0][1]
                        if lines_intersect_x and lines_intersect_y:
                            self.kill()
                            return
        else:
            for player in players:
                lines = player.lines[:-2] if player.id == self.id else player.lines
                for line in lines:
                    line_is_vertical = line[0][0] == line[1][0]
                    if line_is_vertical:
                        lines_intersect_y = line[0][1] <= recent[0][1] <= line[1][1] or line[1][1] <= recent[0][1] <= line[0][1]
                        lines_intersect_x = recent[0][0] <= line[0][0] <= recent[1][0] or recent[1][0] <= line[0][0] <= recent[0][0]
                        if lines_intersect_y and lines_intersect_x:
                            self.kill()
                            return
                    else:
                        lines_intersect_y = line[0][1] == recent[0][1]
                        lines_intersect_x = line[0][0] <= recent[1][0] <= line[1][0] or line[1][0] <= recent[1][0] <= line[0][0]
                        if lines_intersect_y and lines_intersect_x:
                            self.kill()
                            return
        self.recent = recent

    def shorten(self):
        if self.length >= self.desired_length:
            last = self.lines[0]
            last_is_vertical = last[0][0] == last[1][0]
            if last_is_vertical:
                last_is_up = last[0][1] > last[1][1]
                if last_is_up:
                    last[0][1] -= self.velocity
                else:
                    last[0][1] += self.velocity
                if last[0][1] == last[1][1]:
                    self.lines.pop(0)
                    return
            else:
                last_is_left = last[0][0] > last[1][0]
                if last_is_left:
                    last[0][0] -= self.velocity
                else:
                    last[0][0] += self.velocity
                if last[0][0] == last[1][0]:
                    self.lines.pop(0)
                    return
            self.lines[0] = last
        else:
            self.length += self.velocity

    def kill(self):
        self.is_alive = False
        self.color = (112, 18, 18)

    def get_head(self):
        return self.lines[-1][1]

    def draw(self, screen):
        for line in self.lines:
            pygame.draw.lines(screen, [0, 0, 0], False, line, 5)

        for line in self.lines:
            pygame.draw.lines(screen, self.color, False, line, 3)

        if self.is_alive:
            head = self.get_head()
            screen.blit(bikes[self.direction], (head[0] - 8, head[1] - 8))


class Button:
    instances = []

    def __init__(self, x, y, width, height, color):
        self.__class__.instances.append(self)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.dark = (min(x + 20, 255) for x in color)
        self.selected = False

    def is_in(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen, inside):
        color = self.dark if inside else self.color
        pygame.draw.rect(screen, color, self.rect)


class UserInput(Button):
    def __init__(self):
        super().__init__(Button)
        self.string = ""

    def click(self):
        keys = pygame.key.get_pressed()
