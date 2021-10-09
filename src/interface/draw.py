from typing import List

import pygame as pg

from logic.game import Game, Spot, Tower, Projectile
from logic.towers import BaseTower, ShortRangeTower, LongRangeTower, MiningTower
from interface.control import KeyboardController
import interface.control as control
from logic import consts


class Drawer:
    def __init__(self, screen: pg.Surface, game: Game,
                 controllers: tuple[KeyboardController, KeyboardController]):
        self.screen = screen
        self.game = game
        self.controllers = controllers

        self.big_font = pg.font.SysFont('Comic Sans MS', 30)
        self.small_font = pg.font.SysFont('Comic Sans MS', 12)

    def draw_game(self):
        self.draw_background()

        self.draw_graph(self.game.spots)
        self.draw_projectiles(self.game.projectiles)
        self.draw_towers(self.game.spots)

        self.draw_pointers()
        self.draw_interface()

        pg.display.flip()

    def draw_background(self):
        self.screen.fill(pg.Color(150, 200, 150))

    def draw_graph(self, spots: list[Spot]):
        # draw lines
        for s1 in spots:
            for s2 in s1.neighbours:
                pg.draw.line(
                    surface=self.screen,
                    color=pg.Color(200, 200, 200),  # light grey
                    start_pos=s1.pos,
                    end_pos=s2.pos,
                    width=5
                )

        # draw spots
        for s in spots:
            pg.draw.circle(
                surface=self.screen,
                color=pg.Color(125, 125, 125),  # grey
                center=s.pos,
                radius=consts.TOWER_RADIUS
            )

    def draw_projectiles(self, projectiles: list[Projectile]):
        for p in projectiles:
            pg.draw.circle(
                surface=self.screen,
                color=pg.Color(250, 250, 100),  # yellow
                center=p.pos,
                radius=5
            )

    def draw_towers(self, spots: list[Spot]):
        for s in spots:
            if s.tower is not None:
                self.draw_tower(s.tower)
                self.draw_hp_bar(s.tower)

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

    def draw_interface(self):
        self.draw_box()
        self.draw_stats()
        self.draw_icons()

    def draw_box(self):
        # Player 1 half
        rects1 = [
            pg.Rect(0, 0, 50, 800),
            pg.Rect(0, 0, 500, 50),
            pg.Rect(0, 650, 500, 150)
        ]
        # Player 2 half
        rects2 = [
            pg.Rect(950, 0, 50, 800),
            pg.Rect(500, 0, 500, 50),
            pg.Rect(500, 650, 500, 150)
        ]
        # Common (timer)
        rects3 = [
            pg.Rect(400, 0, 200, 50)
        ]
        for rect in rects1:
            pg.draw.rect(
                surface=self.screen,
                color=pg.Color(150, 50, 50),  # dark red
                rect=rect
            )
        for rect in rects2:
            pg.draw.rect(
                surface=self.screen,
                color=pg.Color(50, 50, 150),  # dark blue
                rect=rect
            )
        for rect in rects3:
            pg.draw.rect(
                surface=self.screen,
                color=pg.Color(200, 200, 100),  # yellow
                rect=rect
            )

    def draw_stats(self):
        # Player 1 money
        pic1 = self.big_font.render(
            "Money " + str(self.game.player_one.money),
            False,
            pg.Color(255, 255, 255),  # white
        )
        self.screen.blit(
            pic1,
            (100, 10),
        )

        # Player 2 money
        pic2 = self.big_font.render(
            "Money " + str(self.game.player_two.money),
            False,
            pg.Color(255, 255, 255),  # white
        )
        self.screen.blit(pic2, (900 - pic2.get_width(), 10))

        # Time
        time_in_sec = self.game.time // consts.FPS
        sec = time_in_sec % 60
        mins = time_in_sec // 60
        time_str = str(mins) + "m" + str(sec) + "s"
        pic_time = self.big_font.render(
            time_str,
            False,
            pg.Color(255, 255, 255),  # white
        )
        self.screen.blit(pic_time, (500 - pic_time.get_width() // 2, 10))

    def draw_icons(self):
        y_start = 680
        x_step = 100

        for pid in [0, 1]:
            player = self.game.players[pid]
            x_border = pid * 500 + 50

            cnt: KeyboardController = self.controllers[pid]
            if cnt.sup_pointer is not None:
                self.draw_icon(
                    pg.Vector2(x_border, y_start),
                    'Accept',
                    ['Accept'],
                    is_ready=True
                )
                self.draw_icon(
                    pg.Vector2(x_border + x_step, y_start),
                    'Decline',
                    ['Decline'],
                    is_ready=True
                )
            elif cnt.pointer.tower is None:
                pass
            elif cnt.pointer.tower.player == player:
                pass
            else:
                pass

    def draw_icon(self, pos: pg.Vector2, symbol: str, description: List[str], is_ready: bool):
        pos = pg.Vector2(pos)

        # fill back
        if is_ready:
            draw_color = pg.Color(250, 250, 250)  # white
            fill_color = pg.Color(170, 170, 170)  # light grey
        else:
            draw_color = pg.Color(250, 250, 250)  # white
            fill_color = pg.Color(100, 100, 100)  # dark grey
        pg.draw.rect(
            self.screen,
            fill_color,
            pg.Rect(pos, (70, 70)),
        )

        # icon symbol
        self.draw_action_sym(pos, symbol, draw_color)

        # icon frame
        pg.draw.rect(
            self.screen,
            draw_color,
            pg.Rect(pos, (70, 70)),
            3
        )

        # description below
        text = '\n'.join(description)
        text_pic = self.small_font.render(
            text,
            False,
            pg.Color(250, 250, 250)  # white
        )
        self.screen.blit(
            text_pic,
            pos + pg.Vector2(0, 80)
        )

    @staticmethod
    def get_action_button(action: control.Action, pid: int):
        keys_dict = control.BUTTONS_BY_PLAYER[pid-1]

        for key in keys_dict:
            if action in keys_dict[key]:
                return key

    def draw_action_sym(self, pos: pg.Vector2, name: str, color: pg.Color):
        # size = (70, 70)
        if name == 'Accept':
            pg.draw.line(
                self.screen,
                color,
                pos + pg.Vector2(10, 10),
                pos + pg.Vector2(35, 60),
            )
            pg.draw.line(
                self.screen,
                color,
                pos + pg.Vector2(60, 10),
                pos + pg.Vector2(35, 60),
            )
        elif name == 'Decline':
            pg.draw.line(
                self.screen,
                color,
                pos + pg.Vector2(10, 10),
                pos + pg.Vector2(60, 60),
            )
            pg.draw.line(
                self.screen,
                color,
                pos + pg.Vector2(60, 10),
                pos + pg.Vector2(10, 60),
            )
        else:
            raise RuntimeError(f"Unknown action name: {name}")

    BUTTON_NAMES = {
        pg.K_KP0: '0', pg.K_KP1: '1', pg.K_KP2: '2', pg.K_KP3: '3', pg.K_KP4: '4',
        pg.K_KP5: '5', pg.K_KP6: '6', pg.K_KP7: '7', pg.K_KP8: '8', pg.K_KP9: '9',
        pg.K_t: 't', pg.K_y: 'y', pg.K_u: 'u', pg.K_g: 'g', pg.K_h: 'h',
    }
