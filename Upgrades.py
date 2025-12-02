from __future__ import annotations
from GameObjects import GameObject, Player, Snowball
import pygame
import math

class Upgrade():
    def __init__(self, name:str, cooldownDuration:int, event:int, upgrades:list[Upgrade]) -> None:
        self.name = name
        self.cooldownDuration = cooldownDuration
        self.event = event
        pygame.time.set_timer(self.event, cooldownDuration * 1000)
        upgrades.append(self)

    def action(self, player:Player, gameObjects:list[GameObject]) -> None:
        pass

class DefaultUpgrade(Upgrade):
    def __init__(self, upgrades:list[Upgrade]):
        self.event = pygame.USEREVENT + 1
        Upgrade.__init__(self, "Default", 3, self.event, upgrades)
    
    def action(self, player:Player, gameObjects:list[GameObject]) -> None:
        Snowball(player.x, player.y, 0, gameObjects)
        Snowball(player.x, player.y, math.pi/4, gameObjects)
        Snowball(player.x, player.y, math.pi/2, gameObjects)
        Snowball(player.x, player.y, math.pi*3/4, gameObjects)
        Snowball(player.x, player.y, math.pi, gameObjects)
        Snowball(player.x, player.y, math.pi*5/4, gameObjects)
        Snowball(player.x, player.y, math.pi*3/2, gameObjects)
        Snowball(player.x, player.y, math.pi*7/4, gameObjects)