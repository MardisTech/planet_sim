from ctypes.wintypes import POINT
from turtle import width
import pygame
import math
pygame.init()

# BIG THANKS TO 'TECH WITH TIM' FOR THE YOUTUBE TUTORIAL ON THE TEMPLATE
# ADDITIONAL CODE ADDED BY ALEX MARDIS 

WIDTH, HEIGHT = 1600, 1000 # originally at  800 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Orbits Simulation (To Scale)")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
DARK_GRAY = (80, 78, 81)
ORANGE = (255, 165, 0)
TAN = (188,152,126)
BABY_BLUE = (137, 207, 240)
DARK_BLUE =  (32, 42, 68)

FONT = pygame.font.SysFont("comic sans", 15)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 25 / AU   # 1 AU = 100 PIXELS @  250 / AU
    TIMESTEP = 3600*24 # 1 DAY IN SECONDS

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y 
        self.radius = radius 
        self.color = color 
        self.mass = mass

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []
        
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 2) 

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000), 1}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/2))

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 7.5, YELLOW, 1.98892 * 10**30) #(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 4, BLUE, 5.9742 * 10**24) #(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 3, RED, 6.39 * 10**23) #(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 2, DARK_GRAY, 3.30 * 10**23) #0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10**23
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 3.5, WHITE, 4.8685 * 10**24) #0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24
    venus.y_vel = -35.02 * 1000
    
    jupiter = Planet(-5.2 * Planet.AU, 0, 14, ORANGE, 1898.13 * 10**24)
    jupiter.y_vel = 13.07 * 1000

    saturn = Planet(9.5 * Planet.AU, 0, 12, TAN, 5.683 * 10**26)
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(-19.8 * Planet.AU, 0, 10, BABY_BLUE, 8.6 * 10**25)
    uranus.y_vel = 6.8 * 1000

    neptune = Planet(30 * Planet.AU, 0, 9,  DARK_BLUE, 1.024 * 10**24)
    neptune.y_vel = -5.43 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    
    pygame.quit()

main()