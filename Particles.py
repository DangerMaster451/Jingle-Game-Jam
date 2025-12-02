from __future__ import annotations
import pygame
import random

class Particle():
    def __init__(self, x:float, y:float, color:tuple[int,int,int], size:int, lifetime:int, particles:list[Particle]) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        particles.append(self)

    def render(self, screen:pygame.Surface, particles:list[Particle]) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        self.lifetime -= 1
        if self.lifetime < 0:
            particles.remove(self)

class Blood(Particle):
    def __init__(self, x:float, y:float, lifetime:int, particles:list[Particle]) -> None:
        if random.randint(0, 10) == 10:
            color = (random.randint(220,255), random.randint(220,255), random.randint(220,255))
        else:  
            color = (random.randint(100,255), 0, 0)
        super().__init__(x, y, color, 5, lifetime, particles)

class IceBlood(Particle):
    def __init__(self, x:float, y:float, lifetime:int, particles:list[Particle]) -> None:
        if random.randint(1, 4) == 1:
            color = (15, 244, 252)
        else:  
            brightness = random.randint(210,255)
            color = (brightness, brightness, brightness)
        super().__init__(x, y, color, 5, lifetime, particles)