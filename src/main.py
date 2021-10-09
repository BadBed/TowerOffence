import pygame as pg

from basics.load import load_from_file
from logic.towers import BaseTower, LongRangeTower, MiningTower, ShortRangeTower
from basics.session import Session


if __name__ == "__main__":
    game = load_from_file("levels/grid.lvl")
    session = Session(game)
    session.set_tower_types([MiningTower, LongRangeTower, ShortRangeTower])
    session.game.player_one.money += 200
    session.game.player_two.money += 200

    session.loop()
