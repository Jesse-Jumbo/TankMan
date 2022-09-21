from src.template.Player import Player


class TestPlayer(object):
    construction = {"_id": 0, "_no": 0, "x": 0, "y": 0, "width": 60, "height": 60}
    player = Player(construction)

    def test_get_xy_pos(self):
        assert type(self.player.get_xy_pos()) == tuple
        assert type(self.player.get_xy_pos()[0]) == int
        assert type(self.player.get_xy_pos()[1]) == int
