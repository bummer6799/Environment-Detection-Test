import pygame
import time
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 30)

circle_pos = [400, 300]
circle_radius = 20
wall_thickness = 50
house_size = (600, 400)


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)


class Ray:
    def __init__(self, x, y, angle):
        self.pos = pygame.math.Vector2(x, y)
        self.dir = pygame.math.Vector2(1, 0)
        self.dir.rotate_ip(angle)
        self.length = None

    def cast(self, wall):
        x1, y1 = wall[0]
        x2, y2 = wall[1]
        x3, y3 = self.pos
        x4, y4 = self.pos + self.dir

        # Calculate the intersection point of the ray with the wall
        denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if denom == 0:
            return False
        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / denom
        u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / denom
        if 0 < t < 1 and u > 0:
            intersection = self.pos + t * self.dir
            self.length = (intersection - self.pos).length()
            return True
        else:
            return False

def display_info(up_length, down_length, left_length, right_length):
    font = pygame.font.Font(None, 30)
    text_color = (255, 255, 255)

    # Display the lengths of the rays that hit the wall
    up_text = font.render("Up: " + str(up_length), True, text_color)
    down_text = font.render("Down: " + str(down_length), True, text_color)
    left_text = font.render("Left: " + str(left_length), True, text_color)
    right_text = font.render("Right: " + str(right_length), True, text_color)

    screen.blit(up_text, (650, 50))
    screen.blit(down_text, (650, 80))
    screen.blit(left_text, (650, 110))
    screen.blit(right_text, (650, 140))

# Set up walls
walls = [
    ((0, 0), (house_size[0], 0)),
    ((house_size[0], 0), (house_size[0], house_size[1])),
    ((house_size[0], house_size[1]), (0, house_size[1])),
    ((0, house_size[1]), (0, 0)),
    ((wall_thickness, wall_thickness), (wall_thickness, house_size[1]-wall_thickness)),
    ((wall_thickness, wall_thickness), (house_size[0]-wall_thickness, wall_thickness)),
    ((house_size[0]-wall_thickness, house_size[1]-wall_thickness), (house_size[0]-wall_thickness, wall_thickness)),
    ((house_size[0]-wall_thickness, house_size[1]-wall_thickness), (wall_thickness, house_size[1]-wall_thickness)),
]

font = pygame.font.Font(None, 30)
circle = pygame.draw.circle(screen, (255, 0, 0), circle_pos, circle_radius)
def cast_rays():
    # Cast rays in 4 directions and calculate the length of the ray that hits the wall
    # Ray in the up direction
    hit = False
    for i in range(circle_pos[1] - circle_radius, 0, -1):
        if i <= wall_thickness or i >= house_size[1] - wall_thickness:
            hit = True
            up_length = circle_pos[1] - i
            break
    if not hit:
        up_length = None

    # Ray in the down direction
    hit = False
    for i in range(circle_pos[1] + circle_radius, house_size[1]):
        if i <= wall_thickness or i >= house_size[1] - wall_thickness:
            hit = True
            down_length = i - circle_pos[1]
            break
    if not hit:
        down_length = None

    # Ray in the left direction
    hit = False
    for i in range(circle_pos[0] - circle_radius, 0, -1):
        if i <= wall_thickness or i >= house_size[0] - wall_thickness:
            hit = True
            left_length = circle_pos[0] - i
            break
    if not hit:
        left_length = None

    # Ray in the right direction
    hit = False
    for i in range(circle_pos[0] + circle_radius, house_size[0]):
        if i <= wall_thickness or i >= house_size[0] - wall_thickness:
            hit = True
            right_length = i - circle_pos[0]
            break
    if not hit:
        right_length = None

    return up_length, down_length, left_length, right_length

def running():
    clock = pygame.time.Clock()
    while True:
        # Get user input and update circle position
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            circle_pos[0] -= 5
        elif keys[pygame.K_RIGHT]:
            circle_pos[0] += 5
        elif keys[pygame.K_UP]:
            circle_pos[1] -= 5
        elif keys[pygame.K_DOWN]:
            circle_pos[1] += 5

        # Cast rays in all four directions and get the lengths of the rays that hit the wall
        up_length, down_length, left_length, right_length = cast_rays()

        # Display the lengths of the rays that hit the wall
        display_info(up_length, down_length, left_length, right_length)

        # Update the screen
        pygame.draw.rect(screen, (255, 255, 255), (wall_thickness, wall_thickness, house_size[0] - 2*wall_thickness, house_size[1] - 2*wall_thickness))
        pygame.draw.rect(screen, (0, 0, 0), (wall_thickness, wall_thickness, house_size[0] - 2*wall_thickness, house_size[1] - 2*wall_thickness), 2)
        pygame.draw.circle(screen, (255, 0, 0), circle_pos, circle_radius)

        pygame.display.update()

        clock.tick(60)

running()

