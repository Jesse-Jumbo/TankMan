import pygame
from env import *


def collide_hit_rect(one: pygame.sprite, two: pygame.sprite):
    return one.hit_rect.colliderect(two.hit_rect)


def collide_with_mobs(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        sprite.collide_with_mobs()

def collide_with_walls(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        sprite.collide_with_walls()


def collide_sprite_with_group2(sprite: pygame.sprite.Sprite, group: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(sprite, group, True, collide_hit_rect)
    for hit in hits:
        pass
