import pygame
from src import TankMan

from mlgame.view.view import PygameView
from mlgame.gamedev.generic import quit_or_esc

FPS = 30
if __name__ == '__main__':
    pygame.init()
    game = TankMan.TankMan(map_no=1, frame_limit=300, sound="off")
    scene_init_info_dict = game.get_scene_init_data()
    game_view = PygameView(scene_init_info_dict)
    frame_count = 0
    while game.is_running() and not quit_or_esc():
        clock = pygame.time.Clock()
        clock.tick_busy_loop(FPS)
        # TODO how set game title
        result = game.update(game.get_keyboard_command())
        game_progress_data = game.get_scene_progress_data()
        game_view.draw(game_progress_data)
        frame_count += 1
        if result == "RESET":
            game.reset()
            game_view.reset()

    pygame.quit()

