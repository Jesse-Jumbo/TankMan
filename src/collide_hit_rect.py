from typing import Optional
import pygame.sprite

from src.Player import Player
from src.Bullet import Bullet
from src.Wall import Wall


def collide_with_walls(group1: pygame.sprite.Group, group2: pygame.sprite.Group):
    hits = pygame.sprite.groupcollide(group1, group2, False, False, pygame.sprite.collide_rect_ratio(0.8))
    for sprite, walls in hits.items():
        sprite.collide_with_walls()


def collide_with_bullets(group1: pygame.sprite.Group, group2: pygame.sprite.Group, green_team_num: Optional[int] = None):
    hits = pygame.sprite.groupcollide(group1, group2, False, False, pygame.sprite.collide_rect_ratio(0.8))
    player_score_data = {}
    for sprite, bullets in hits.items():
        for bullet in bullets:
            if bullet.no != sprite.no and sprite.lives > 0:
                bullet.kill()

                if isinstance(sprite, Player):
                    assert green_team_num is not None
                    if (bullet.no - 1) // green_team_num == (sprite.no - 1) // green_team_num:
                        # -20 for friendly damage
                        score = -20
                    else:
                        score = 20
                elif isinstance(sprite, Wall):
                    score = 1
                    if sprite.lives == 1:
                        score += 5
                else:
                    continue

                sprite.collide_with_bullets()

                if player_score_data.get(bullet.no) is None:
                    player_score_data[bullet.no] = 0
                player_score_data[bullet.no] += score
    return player_score_data


def collide_with_supply_stations(sprites: pygame.sprite.Group, supply_stations: pygame.sprite.Group):
    hits = pygame.sprite.groupcollide(sprites, supply_stations, False, False, pygame.sprite.collide_rect_ratio(0.8))
    for sprite, supply_station in hits.items():
        if isinstance(sprite, Player):
            if supply_station[0].id == 5:
                sprite.get_oil(supply_station[0].power)
            else:
                sprite.get_power(supply_station[0].power)
        elif isinstance(sprite, Bullet):
            sprite.kill()

        supply_station[0].collect()

    return [supply_station[0] for supply_station in hits.values()]
