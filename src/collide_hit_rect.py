import random

import pygame.sprite

from .TankPlayer import TankPlayer
from .env import *


all_pos = []
for x in range(18):
    for y in range(12):
        all_pos.append((50*x, 50*y))


def collide_hit_rect(one: pygame.sprite, two: pygame.sprite):
    return one.hit_rect.colliderect(two.hit_rect)


def collide_with_walls(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        sprite.collide_with_walls()


def collide_with_bullets(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits and hits[0]._id != sprite._id:
        hits[0].kill()
        score = 1
        if sprite.lives == 1:
            score += 5
        sprite.collide_with_bullets()
        return hits[0]._id, score
    return None, None


def collide_with_bullet_stations(player: TankPlayer, stations: pygame.sprite.Group, all_sprite: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(player, stations, False, collide_hit_rect)
    if hits:
        existed_pos = []
        player.get_power(hits[0].get_supply())
        for sprite in all_sprite:
            existed_pos.append(sprite.rect.topleft)
        new_pos = list(set(all_pos) - set(existed_pos))
        hits[0].rect.topleft = random.choice(new_pos)
        hits[0].hit_rect.center = hits[0].rect.center


def collide_with_oil_stations(player: TankPlayer, stations: pygame.sprite.Group, all_sprite: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(player, stations, False, collide_hit_rect)
    if hits:
        existed_pos = []
        player.get_oil(hits[0].get_supply())
        for sprite in all_sprite:
            existed_pos.append(sprite.rect.topleft)
        new_pos = list(set(all_pos) - set(existed_pos))
        hits[0].rect.topleft = random.choice(new_pos)
        hits[0].hit_rect.center = hits[0].rect.center
