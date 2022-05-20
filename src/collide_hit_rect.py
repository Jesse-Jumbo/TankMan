import pygame.sprite

from .TankPlayer import TankPlayer
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


def collide_with_bullet_stations(player: TankPlayer, stations: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(player, stations, False, collide_hit_rect)
    if hits:
        player.get_power(hits[0].get_supply())


def collide_with_oil_stations(player: TankPlayer, stations: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(player, stations, False, collide_hit_rect)
    if hits:
        player.get_oil(hits[0].get_supply())
