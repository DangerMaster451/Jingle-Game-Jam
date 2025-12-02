from GameObjects import GameObject, Player, Enemy, Pickup, Snowball
from Particles import Particle, Blood, IceBlood
from Upgrades import Upgrade, DefaultUpgrade
import pygame
import random
import math


def spawnEnemies(player:Player, enemies:list, max_enemies, spawn_radius):
    if len(enemies) < max_enemies:
        direction = random.randint(0,360)
        x = math.sin(math.radians(direction)) * spawn_radius
        y = math.cos(math.radians(direction)) * spawn_radius
        Enemy(x, y, gameObjects, enemies)

def spawnBloodCloud_Advanced(spawnX:float, spawnY:float, object:GameObject, radius_min:int, radius_max:int, spread:int, count:int) -> None:
    radius = random.randint(radius_min, radius_max)
    for i in range(count):
        direction = random.randint(round(math.degrees(object.direction))-spread, round(math.degrees(object.direction)+spread))
        if direction == 0:
            direction = 1
        distance = (math.degrees(object.direction)+1)/(direction) * radius * random.random()
        x = math.sin(math.radians(direction)) * distance
        y = math.cos(math.radians(direction)) * distance
        lifetime = round(radius_max - distance) * 5
        Blood(spawnX+x, spawnY+y, lifetime, particles)

def spawnBloodCloud(spawnX:float, spawnY:float, radius_min:int, radius_max:int, spread:int, count:int) -> None:
    radius = random.randint(radius_min, radius_max)
    for i in range(count):
        direction = random.randint(0,360)
        distance = random.randint(0, radius)
        x = math.sin(math.radians(direction)) * distance
        y = math.cos(math.radians(direction)) * distance
        lifetime = round(radius_max - distance) * 5
        Blood(spawnX+x, spawnY+y, lifetime, particles)

def spawnIceBloodCloud(spawnX:float, spawnY:float, radius_min:int, radius_max:int, spread:int, count:int) -> None:
    radius = random.randint(radius_min, radius_max)
    for i in range(count):
        direction = random.randint(0,360)
        distance = random.randint(0, radius)
        x = math.sin(math.radians(direction)) * distance
        y = math.cos(math.radians(direction)) * distance
        lifetime = round(radius_max - distance) * 5
        IceBlood(spawnX+x, spawnY+y, lifetime, particles)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

#objects
gameObjects:list[GameObject] = []
upgrades:list[Upgrade] = []
enemies:list[Enemy] = []
particles:list[Particle] = []

p = Player(300,300, gameObjects)
d = DefaultUpgrade(upgrades)

while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for upgrade in upgrades:
            if event.type == upgrade.event:
                upgrade.action(p, gameObjects)

    screen.fill("black")

    for particle in particles:
        particle.render(screen, particles)

    for gameObject in gameObjects:
        gameObject.update_position(dt)
        gameObject.render(screen)

    spawnEnemies(p, enemies, 25, 1000)

    for enemy in enemies:
        enemy.move_toward_object(p, dt)
        o = enemy.check_collisions(gameObjects)
        if o != None and type(o) == Snowball:
            enemy.health -= o.damage
            gameObjects.remove(o)
            if enemy.health <= 0:
                spawnIceBloodCloud(enemy.x, enemy.y, 35, 75, 10, 125)
                Pickup(enemy.x, enemy.y, gameObjects)
                enemies.remove(enemy)
                gameObjects.remove(enemy)

    object = p.check_collisions(gameObjects)
    if type(object) == Enemy:
        spawnBloodCloud(p.x, p.y, 35, 75, 10, 125)
        pygame.time.wait(2000)
        running = False
    elif type(object) == Pickup:
        gameObjects.remove(object)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()