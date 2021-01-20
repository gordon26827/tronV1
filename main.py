import pygame
from classes import *
from network import *

# local ip @UMD is 10.104.17.88

width = 983
height = 598

screen = pygame.display.set_mode((width, height))
pygame.font.init()

pygame.display.set_caption("TRON")
header = pygame.image.load("tron_logo.jpg")
icon = pygame.image.load("tron_icon.jpg")
pygame.display.set_icon(icon)

font = pygame.font.Font('TurretRoad-Regular.ttf', 30)


def draw_board(players, started):
    screen.fill((50, 50, 50))

    for y in range(height//35):
        for x in range(width//35):
            pygame.draw.rect(screen, (7, 18, 43), (x*35 + 3, y*35 + 3, 32, 32))

    for rider in players:
        rider.draw(screen)

    if not started:
        message3 = font.render("Waiting for Host", True, (255, 255, 255))
        screen.blit(message3, (500, 500))

    pygame.display.update()


def draw_menu(text, error):
    text = font.render(text, True, (255, 255, 255))
    help1 = font.render("Enter Server Address:", True, (255, 255, 255))
    help2 = font.render("Press ENTER to Connect", True, (255, 255, 255))

    text.get_size()

    screen.fill((0, 0, 0))
    screen.blit(header, (75, 0))
    pygame.draw.rect(screen, (100, 100, 100), (300, 400, 350, 50))
    screen.blit(text, ((475 - text.get_size()[0]//2), 410))
    screen.blit(help1, (320, 350))
    screen.blit(help2, (305, 470))

    if error:
        message = font.render("Invalid Address Provided", True, (255, 0, 0))
        screen.blit(message, (310, 280))

    pygame.display.update()


def menu():
    running, error = True, False
    text = ""
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        main(text)
                    except:
                        error = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif len(text) < 16:
                    char = event.unicode
                    if char.isnumeric() or char == '.':
                        text += char

        draw_menu(text, error)

def main(ip):
    running, started = True, True
    network = Network(ip)
    me = network.get_p()
    direction, prev_dir = me.direction, me.direction
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)
        players = network.send(me)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and prev_dir != 'S':
                    direction = 'N'

                if event.key == pygame.K_DOWN and prev_dir != 'N':
                    direction = 'S'

                if event.key == pygame.K_RIGHT and prev_dir != 'W':
                    direction = 'E'

                if event.key == pygame.K_LEFT and prev_dir != 'E':
                    direction = 'W'

            if event.type == pygame.QUIT:
                running = False

        draw_board(players, started)

        if started:
            me.move(direction, players)
            prev_dir = direction

menu()