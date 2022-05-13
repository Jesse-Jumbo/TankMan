import pygame.sprite

from .TankStation import TankStation
from .env import *


def collide_hit_rect(one: pygame.sprite, two: pygame.sprite):
    return one.hit_rect.colliderect(two.hit_rect)


def collide_with_walls(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        sprite.collide_with_walls()


def collide_with_bullets(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    for hit in hits:
        if hit._id != sprite._id:
            hit.kill()
            sprite.collide_with_bullets()


def collide_with_stations(player: pygame.sprite.Sprite, stations: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(player, stations, False, collide_hit_rect)
    if hits:
        if hits[0]._id == 4:
            player.power += hits[0].get_power()
        elif hits[0]._id == 5:
            player.oil += hits[0].get_power()
