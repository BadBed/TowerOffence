import pygame as pg

from logic.game import Game, Spot, Tower, Projectile
from logic.towers import BaseTower, ShortRangeTower, LongRangeTower, MiningTower
from interface.control import KeyboardController
from logic import consts


class Drawer:
    def __init__(self, screen: pg.Surface, game: Game,
                 controllers: tuple[KeyboardController, KeyboardController]):
        self.screen = screen
        self.game = game
        self.controllers = controllers

        self.font = pg.font.SysFont('Comic Sans MS', 30)

    def draw_game(self):
        self.draw_background()

        self.draw_graph(self.game.spots)
        self.draw_projectiles(self.game.projectiles)
        self.draw_towers(self.game.spots)

        self.draw_pointers()
        self.draw_interface()

        pg.display.flip()

    def draw_projectiles(self, projectiles: list[Projectile]):
        for p in projectiles:
            pg.draw.circle(
                surface=self.screen,
                color=pg.Color(250, 250, 100),  # yellow
                center=p.pos,
                radius=5
            )

    def draw_background(self):
        self.screen.fill(pg.Color(150, 200, 150))

    def draw_box(self):
        rects = [
            pg.Rect(0, 0, 50, 800),
            pg.Rect(950, 0, 50, 800),
            pg.Rect(0, 0, 1000, 50),
            pg.Rect(0, 650, 1000, 150)
        ]
        for rect in rects:
            pg.draw.rect(
                surface=self.screen,
                color=pg.Color(100, 100, 100),
                rect=rect
            )

    def draw_graph(self, spots: list[Spot]):
        # interface lines
        for s1 in spots:
            for s2 in s1.neighbours:
                pg.draw.line(
                    surface=self.screen,
                    color=pg.Color(200, 200, 200),  # light grey
                    start_pos=s1.pos,
                    end_pos=s2.pos,
                    width=5
                )

        # interface spots
        for s in spots:
            pg.draw.circle(
                surface=self.screen,
                color=pg.Color(125, 125, 125),  # grey
                center=s.pos,
                radius=consts.TOWER_RADIUS
            )

    def draw_towers(self, spots: list[Spot]):
        for s in spots:
            if s.tower is not None:
                self.draw_tower(s.tower)
                self.draw_hp_bar(s.tower)

    def draw_tower(self, tower: Tower):
        pos = tower.spot.pos
        # Body
        if tower.player.id == 1:
            color = pg.Color(200, 150, 150)
        else:
            color = pg.Color(150, 150, 200)
        pg.draw.circle(
            surface=self.screen,
            color=color,
            center=pos,
            radius=consts.TOWER_RADIUS
        )

        # Symbol
        sym_color = pg.Color(250, 250, 250)
        if type(tower) == LongRangeTower:
            pg.draw.line(
                surface=self.screen,
                color=sym_color,
                start_pos=pos + pg.Vector2(0, 15),
                end_pos=pos + pg.Vector2(0, -15),
                width=2,
            )
        elif type(tower) == ShortRangeTower:
            pg.draw.line(
                surface=self.screen,
                color=sym_color,
                start_pos=pos + pg.Vector2(8, 8),
                end_pos=pos + pg.Vector2(-8, -8),
                width=2,
            )
            pg.draw.line(
                surface=self.screen,
                color=sym_color,
                start_pos=pos + pg.Vector2(-8, 8),
                end_pos=pos + pg.Vector2(8, -8),
                width=2,
            )
        elif type(tower) == MiningTower:
            pg.draw.line(
                surface=self.screen,
                color=sym_color,
                start_pos=pos + pg.Vector2(0, 8),
                end_pos=pos + pg.Vector2(0, -8),
                width=2,
            )
            pg.draw.circle(
                surface=self.screen,
                color=sym_color,
                center=pos,
                radius=10,
                width=2,
            )

    def draw_hp_bar(self, tower: Tower):
        frac = tower.hp / tower.MAX_HP
        center = tower.spot.pos
        pg.draw.rect(
            surface=self.screen,
            color=pg.Color(250, 0, 0),
            rect=pg.Rect(center + pg.Vector2(-20, -45), (40, 10))
        )
        pg.draw.rect(
            surface=self.screen,
            color=pg.Color(0, 250, 0),
            rect=pg.Rect(center + pg.Vector2(-20, -45), (40 * frac, 10))
        )

    def draw_money(self):
        # Player 1
        pic1 = self.font.render(
            "Money " + str(self.game.player_one.money),
            False,
            pg.Color(255, 255, 255),  # white
        )
        self.screen.blit(
            pic1,
            (100, 10),
        )

        # Player 2
        pic2 = self.font.render(
            "Money " + str(self.game.player_two.money),
            False,
            pg.Color(255, 255, 255),  # white
        )
        self.screen.blit(
            pic2,
            (800, 10),
        )

    def draw_interface(self):
        self.draw_box()
        self.draw_money()

    def draw_pointers(self):
        colors = [
            pg.Color(250, 0, 0),  # red
            pg.Color(0, 0, 250),  # blue
        ]
        sup_colors = [
            pg.Color(200, 0, 0),  # dark red
            pg.Color(0, 0, 200),  # dark blue
        ]

        for pid in [0, 1]:
            cnt: KeyboardController = self.controllers[pid]

            dr = 0
            if self.controllers[0].pointer == self.controllers[1].pointer:
                dr = 2*pid

            pg.draw.circle(
                surface=self.screen,
                color=colors[pid],
                center=cnt.pointer.pos,
                radius=consts.TOWER_RADIUS + dr,
                width=2
            )
            if cnt.sup_pointer is not None:
                pg.draw.circle(
                    surface=self.screen,
                    color=sup_colors[pid],
                    center=cnt.sup_pointer.spot.pos,
                    radius=consts.TOWER_RADIUS + 5,
                    width=2
                )

