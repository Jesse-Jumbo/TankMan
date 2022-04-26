import pygame.sprite

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
        if hit._no != sprite._no:
            hit.kill()
            sprite.collide_with_bullets()


def collide_bullets_with_walls(bullets: pygame.sprite.Group, walls: pygame.sprite.Group):
    hits = pygame.sprite.groupcollide(bullets, walls, True, False, collide_hit_rect)