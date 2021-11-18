import pygame

# MINECRAFT COLORS
BLACK = (0, 0, 0)
GRAY = (96, 96, 96)
LGRAY = (192, 192, 192)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 32
HEIGHT = 18

class Pixel():
    def __init__(self, x, y, anim, size=10):
        self.x = x
        self.y = y
        self.anim = anim
        self.size = size
        self.frame = 0

    def draw(self):
        """ Draws the current frame """
        color_string = self.anim[self.frame]
        color = RED
        if color_string == "0":
            color = BLACK
        elif color_string == "7":
            color = GRAY
        elif color_string == "8":
            color = LGRAY
        elif color_string == "f":
            color = WHITE
        pygame.draw.rect(screen, color, [self.x * self.size, self.y * self.size, self.size, self.size])
        self.frame += 1


# file setup
file = open("badapplePyTest.nut", "r")
all_animations = file.readlines()
all_animations = all_animations[::-1]

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH * 10, HEIGHT * 10))
pygame.display.set_caption('Video Test')
clock = pygame.time.Clock()

pixel_list = []

current_x = 0
current_y = 0
for line in all_animations:
    pixel_list.append(Pixel(current_x, current_y, line, 10))

    current_x += 1

    if current_x >= WIDTH:
        current_x = 0
        current_y += 1


done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # fill the screen with background color
    screen.fill(WHITE)

    # draw here:
    for p in pixel_list:
        p.draw()

    # update the screen
    pygame.display.update()
    clock.tick(20)

pygame.quit()
