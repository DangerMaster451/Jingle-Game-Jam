import pygame
import math
import random

class GameObject():
    def __init__(self, x:float=0, y:float=0, direction:float=0, speed:int=300, hitboxRadius:int=50, imagePath:str="", imageSize:tuple[int,int]=(50,50)) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.hitboxRadius = hitboxRadius
        self.image = self.loadImage(imagePath, imageSize)
        gameObjects.append(self)

    def update_position(self) -> None:
        pass

    def render(self, screen:pygame.Surface) -> None:
        pygame.Surface.blit(screen, self.image, (self.x, self.y))
    
    def loadImage(self, path:str, size:tuple[int,int]) -> pygame.Surface:
        return pygame.transform.scale(pygame.image.load(path), size)
    
    def move_toward_object(self, object) -> None:
        self.direction = math.atan2((object.y - self.y), (object.x - self.x)) + math.pi/2
        self.x += math.sin(self.direction) * self.speed * dt
        self.y -= math.cos(self.direction) * self.speed * dt

    def getDistanceBetweenObjects(self, objectA, objectB) -> float:
        return math.sqrt((objectB.y - objectA.y)**2 + (objectB.x - objectA.x)**2)

class Player(GameObject):
    def __init__(self, x:float, y:float) -> None:
       self.health = 100
       GameObject.__init__(self, x, y, 0, 100, 30, "Assets/Evil Snowman.png", (100,100))

    def update_position(self) -> None:
        mouseX, mouseY = pygame.mouse.get_pos()
        self.direction = math.atan2((mouseY - self.y), (mouseX - self.x)) + math.pi/2
        self.x += math.sin(self.direction) * self.speed * dt
        self.y -= math.cos(self.direction) * self.speed * dt

    def check_collisions(self, objects) -> GameObject | None:
        for object in objects:
            if self.getDistanceBetweenObjects(self, object) < self.hitboxRadius + object.hitboxRadius:
                if object != self:
                    return object
        return None

    def render(self, screen:pygame.Surface):
        pygame.draw.circle(screen, "cornsilk1", (self.x, self.y), self.hitboxRadius)

class Snowball(GameObject):
    def __init__(self, x:float, y:float, direction:float) -> None:
        self.damage = 15
        super().__init__(x, y, direction, 300, 15, "Assets/Snowball.png")

    def update_position(self) -> None:
        self.x += math.sin(self.direction) * self.speed * dt
        self.y -= math.cos(self.direction) * self.speed * dt

    def render(self, screen:pygame.Surface):
        pygame.draw.circle(screen, "cyan", (self.x, self.y), 15)

class Enemy(GameObject):
    def __init__(self, x:float, y:float):
        self.health = 30
        super().__init__(x, y, 0, 75, 20, "Assets/Evil Snowman.png", (100,100))
        enemies.append(self)

    def check_collisions(self, gameObjects) -> GameObject | None:
        for object in gameObjects:
            if type(object) == Snowball:
                if self.getDistanceBetweenObjects(self, object) < self.hitboxRadius + object.hitboxRadius:
                    return object
        return None

    def render(self, screen:pygame.Surface):
        pygame.draw.circle(screen, "white", (self.x, self.y), 20)

class Pickup(GameObject):
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x, y, 0, 0, 15, "Assets/Player.png", (15,15))

    def check_collisions(self, gameObjects) -> bool:
        for object in gameObjects:
            if type(object) == Player:
                if self.getDistanceBetweenObjects(self, object) < self.hitboxRadius + object.hitboxRadius:
                    return True
        return False
    
    def render(self, screen:pygame.Surface):
        pygame.draw.circle(screen, "green4", (self.x, self.y), 10)

class Upgrade():
    def __init__(self, name:str, cooldownDuration:int, event:int) -> None:
        self.name = name
        self.cooldownDuration = cooldownDuration
        pygame.time.set_timer(event, cooldownDuration * 1000)
        upgrades.append(self)

    def action(self, player:Player) -> None:
        pass

class DefaultUpgrade(Upgrade):
    def __init__(self):
        self.event = pygame.USEREVENT + 1
        Upgrade.__init__(self, "Default", 3, self.event)
    
    def action(self, player:Player):
        Snowball(player.x, player.y, 0)
        Snowball(player.x, player.y, math.pi/4)
        Snowball(player.x, player.y, math.pi/2)
        Snowball(player.x, player.y, math.pi*3/4)
        Snowball(player.x, player.y, math.pi)
        Snowball(player.x, player.y, math.pi*5/4)
        Snowball(player.x, player.y, math.pi*3/2)
        Snowball(player.x, player.y, math.pi*7/4)

class Particle():
    def __init__(self, x:float, y:float, color:tuple[int,int,int], size:int, lifetime:int) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        particles.append(self)

    def render(self, screen:pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        self.lifetime -= 1
        if self.lifetime < 0:
            particles.remove(self)

class Blood(Particle):
    def __init__(self, x:float, y:float, lifetime:int) -> None:
        if random.randint(0, 10) == 10:
            color = (random.randint(220,255), random.randint(220,255), random.randint(220,255))
        else:  
            color = (random.randint(100,255), 0, 0)
        super().__init__(x, y, color, 5, lifetime)

class IceBlood(Particle):
    def __init__(self, x:float, y:float, lifetime:int) -> None:
        if random.randint(1, 4) == 1:
            color = (15, 244, 252)
        else:  
            brightness = random.randint(210,255)
            color = (brightness, brightness, brightness)
        super().__init__(x, y, color, 5, lifetime)

def spawnEnemies(player:Player, enemies:list, max_enemies, spawn_radius):
    if len(enemies) < max_enemies:
        direction = random.randint(0,360)
        x = math.sin(math.radians(direction)) * spawn_radius
        y = math.cos(math.radians(direction)) * spawn_radius
        Enemy(x, y)

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
        Blood(spawnX+x, spawnY+y, lifetime)

def spawnBloodCloud(spawnX:float, spawnY:float, radius_min:int, radius_max:int, spread:int, count:int) -> None:
    radius = random.randint(radius_min, radius_max)
    for i in range(count):
        direction = random.randint(0,360)
        distance = random.randint(0, radius)
        x = math.sin(math.radians(direction)) * distance
        y = math.cos(math.radians(direction)) * distance
        lifetime = round(radius_max - distance) * 5
        Blood(spawnX+x, spawnY+y, lifetime)

def spawnIceBloodCloud(spawnX:float, spawnY:float, radius_min:int, radius_max:int, spread:int, count:int) -> None:
    radius = random.randint(radius_min, radius_max)
    for i in range(count):
        direction = random.randint(0,360)
        distance = random.randint(0, radius)
        x = math.sin(math.radians(direction)) * distance
        y = math.cos(math.radians(direction)) * distance
        lifetime = round(radius_max - distance) * 5
        IceBlood(spawnX+x, spawnY+y, lifetime)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

#objects
gameObjects = []
upgrades = []
enemies = []
particles = []

p = Player(300,300)
d = DefaultUpgrade()

while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for upgrade in upgrades:
            if event.type == upgrade.event:
                upgrade.action(p)

    screen.fill("black")

    for particle in particles:
        particle.render(screen)

    for gameObject in gameObjects:
        gameObject.update_position()
        gameObject.render(screen)

    spawnEnemies(p, enemies, 25, 1000)

    for enemy in enemies:
        enemy.move_toward_object(p)
        o = enemy.check_collisions(gameObjects)
        if o != None:
            enemy.health -= o.damage
            gameObjects.remove(o)
            if enemy.health <= 0:
                spawnIceBloodCloud(enemy.x, enemy.y, 35, 75, 10, 125)
                Pickup(enemy.x, enemy.y)
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