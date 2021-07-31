import pygame as pg

from logic.game import Game
from interface.draw import Drawer
from logic import consts
from interface.control import KeyboardController


class Session:
    def __init__(self, game: Game):
        self.game = game

        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode((1000, 800))
        self.controller_one = KeyboardController(self.screen, game, game.player_one)
        self.controller_two = KeyboardController(self.screen, game, game.player_two)
        self.drawer = Drawer(self.screen, game, (self.controller_one, self.controller_two))

        self.frame_time = round(1000 / consts.FPS)
        self.ts = pg.time.get_ticks()
        self.is_finished = False

    def frame(self):
        self._handle_controls()
        self.game.update()
        self.drawer.draw_game()
        self._wait()

    def loop(self):
        while not self.is_finished:
            self.frame()

    def _wait(self):
        # TODO: dynamic frametime
        ts = pg.time.get_ticks()
        wait_time = self.frame_time - (ts - self.ts)
        # print(f"wait time = {wait_time}")
        if wait_time > 0:
            pg.time.wait(wait_time)
        self.ts = pg.time.get_ticks()

    def _handle_controls(self):
        buttons = list(map(
            lambda e: e.key,
            pg.event.get(pg.KEYDOWN)
        ))

        self.controller_one.handle(buttons)
        self.controller_two.handle(buttons)

        if pg.K_ESCAPE in buttons:
            self.is_finished = True

    def set_tower_types(self, tower_types):
        self.game.player_one.set_tower_types(tower_types)
        self.game.player_two.set_tower_types(tower_types)
