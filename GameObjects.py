from __future__ import annotations
import pygame
import math

class GameObject():
    def __init__(self, x:float, y:float, direction:float, speed:int, hitboxRadius:int, imagePath:str, imageSize:tuple[int,int], gameObjects:list[GameObject]) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.hitboxRadius = hitboxRadius
        self.image = self.loadImage(imagePath, imageSize)
        gameObjects.append(self)

    def update_position(self, dt:float) -> None:
        pass

    def render(self, screen:pygame.Surface) -> None:
        pygame.Surface.blit(screen, self.image, (self.x, self.y))
    
    def loadImage(self, path:str, size:tuple[int,int]) -> pygame.Surface:
        return pygame.transform.scale(pygame.image.load(path), size)
    
    def move_toward_object(self, object, dt:float) -> None:
        self.direction = math.atan2((object.y - self.y), (object.x - self.x)) + math.pi/2
        self.x += math.sin(self.direction) * self.speed * dt
        self.y -= math.cos(self.direction) * self.speed * dt

    def getDistanceBetweenObjects(self, objectA, objectB) -> float:
        return math.sqrt((objectB.y - objectA.y)**2 + (objectB.x - objectA.x)**2)
    
    def check_collisions(self, objects) -> GameObject | None:
        for object in objects:
            if self.getDistanceBetweenObjects(self, object) < self.hitboxRadius + object.hitboxRadius:
                if object != self:
                    return object
        return None

class Player(GameObject):
    def __init__(self, x:float, y:float, gameObjects:list[GameObject]) -> None:
       self.health = 100
       super().__init__(x, y, 0, 100, 30, "Assets/Evil Snowman.png", (100,100), gameObjects)

    def update_position(self, dt:float) -> None:
        mouseX, mouseY = pygame.mouse.get_pos()
        self.direction = math.atan2((mouseY - self.y), (mouseX - self.x)) + math.pi/2
        self.x += math.sin(self.direction) * self.speed * dt
        self.y -= math.cos(self.direction) * self.speed * dt

    def render(self, screen:pygame.Surface):
        pygame.draw.circle(screen, "cornsilk1", (self.x, self.y), self.hitboxRadius)

class Snowball(GameObject):
    def __init__(self, x:float, y:float, direction:float, gameObjects:list[GameObject]) -> None:
        self.damage = 15
        super().__init__(x, y, direction, 300, 15, "Assets/Snowball.png", (30,30), gameObjects)

    def update_position(self, dt:float) -> None:
        self.x += math.sin(self.direction) * self.speed * dt
        self.y -= math.cos(self.direction) * self.speed * dt

    def render(self, screen:pygame.Surface):
        pygame.draw.circle(screen, "cyan", (self.x, self.y), 15)

class Enemy(GameObject):
    def __init__(self, x:float, y:float, gameObjects:list[GameObject], enemies:list[Enemy]):
        self.health = 30
        self.damage = 25
        super().__init__(x, y, 0, 75, 20, "Assets/Evil Snowman.png", (100,100), gameObjects)
        enemies.append(self)

    def render(self, screen:pygame.Surface):
        pygame.draw.circle(screen, "white", (self.x, self.y), 20)

class Pickup(GameObject):
    def __init__(self, x:float, y:float, gameObjects:list[GameObject]) -> None:
        super().__init__(x, y, 0, 0, 15, "Assets/Player.png", (15,15), gameObjects)
    
    def render(self, screen:pygame.Surface):
        pygame.draw.circle(screen, "green4", (self.x, self.y), 10)