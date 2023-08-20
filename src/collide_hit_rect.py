import pygame.sprite

from src.Player import Player
from src.Bullet import Bullet


def collide_with_walls(group1: pygame.sprite.Group, group2: pygame.sprite.Group):
    hits = pygame.sprite.groupcollide(group1, group2, False, False, pygame.sprite.collide_rect_ratio(0.8))
    for sprite, walls in hits.items():
        sprite.collide_with_walls()


def collide_with_bullets(group1: pygame.sprite.Group, group2: pygame.sprite.Group):
    hits = pygame.sprite.groupcollide(group1, group2, False, False, pygame.sprite.collide_rect_ratio(0.8))
    player_score_data = {}
    for sprite, bullets in hits.items():
        for bullet in bullets:
            if bullet.no != sprite.no and sprite.lives > 0:
                bullet.kill()
                score = 1
                if sprite.lives == 1:
                    score += 5
                sprite.collide_with_bullets()

                if player_score_data.get(bullet.no) is None:
                    player_score_data[bullet.no] = 0
                player_score_data[bullet.no] += score
    return player_score_data


def collide_with_stations(sprites: pygame.sprite.Group, stations: pygame.sprite.Group):
    hits = pygame.sprite.groupcollide(sprites, stations, False, False, pygame.sprite.collide_rect_ratio(0.8))
    for sprite, stations in hits.items():
        if isinstance(sprite, Player):
            sprite.get_oil(stations[0].power)
        elif isinstance(sprite, Bullet):
            sprite.kill()

        stations[0].collect()
        return stations
