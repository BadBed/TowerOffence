from enum import Enum
from typing import Optional

import pygame as pg

from logic.game import Game, Player, Spot, Tower


class Action(Enum):
    MOVE_LEFT = "L"
    MOVE_RIGHT = "R"
    MOVE_UP = "U"
    MOVE_DOWN = "D"

    TOWER_1 = "T1"
    TOWER_2 = "T2"
    TOWER_3 = "T3"

    ORDER_1 = "O1"
    ORDER_2 = "O2"
    ORDER_3 = "O3"

    ACCEPT = "OK"
    DECLINE = "NOK"


class KeyboardController:
    def __init__(self, screen: pg.Surface, game: Game, player: Player):
        self.screen = screen
        self.game = game
        self.player = player

        self.moves: dict[(str, Spot), Spot] = game.controller_moves
        self.pointer: Spot = self.game.spots[0]
        self.buttons: dict[int, list[Action]] = BUTTONS_BY_PLAYER[player.id]

        self.sup_pointer: Optional[Tower] = None
        self.sup_action_ind: Optional[int] = None

    def handle(self, buttons):
        if self.sup_pointer is not None and not self.sup_pointer.is_alive():
            self.sup_pointer = None
            self.sup_action_ind = None

        for b in buttons:
            if b not in self.buttons:
                continue
            for action in self.buttons[b]:
                if action in ACTIONS_MOVE:
                    self.pointer = self.moves[(action.value, self.pointer)]
                if self.sup_pointer is None:
                    if action in ACTIONS_TOWER and self.pointer.tower is None:
                        tower_type = self.player.tower_types[ACTION_INDICES[action]-1]
                        self.pointer.ask_build_tower(tower_type, self.player)
                        break
                    if action in ACTIONS_ORDER \
                            and self.pointer.tower is not None \
                            and self.pointer.tower.player == self.player:
                        ind = ACTION_INDICES[action]
                        typ = self.pointer.tower.ask_order_type(ind)
                        if typ == Tower.OrderType.UNDIR:
                            self.pointer.tower.ask_order(ind)
                        if typ == Tower.OrderType.DIR:
                            self.sup_pointer = self.pointer.tower
                            self.sup_action_ind = ind
                        break
                    elif action in ACTIONS_ORDER \
                            and self.pointer.tower is not None \
                            and self.pointer.tower.player != self.player \
                            and action == Action.ORDER_1:
                        for s in self.game.spots:
                            if s.tower is not None \
                                    and s.tower.player == self.player:
                                s.tower.ask_set_target(self.pointer.tower)
                else:
                    if action == Action.DECLINE:
                        self.sup_pointer = None
                        self.sup_action_ind = None
                        break
                    if action == Action.ACCEPT:
                        self.sup_pointer.ask_order(self.sup_action_ind, self.pointer)
                        self.sup_pointer = None
                        self.sup_action_ind = None
                        break


ACTIONS_MOVE = {
    Action.MOVE_UP, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.MOVE_RIGHT
}
ACTIONS_TOWER = [
    Action.TOWER_1, Action.TOWER_2, Action.TOWER_3
]
ACTIONS_ORDER = [
    Action.ORDER_1, Action.ORDER_2, Action.ORDER_3
]
ACTION_INDICES = {
    Action.TOWER_1: 1, Action.TOWER_2: 2, Action.TOWER_3: 3,
    Action.ORDER_1: 1, Action.ORDER_2: 2, Action.ORDER_3: 3
}

BUTTONS_P1 = {
    pg.K_a: [Action.MOVE_LEFT],
    pg.K_d: [Action.MOVE_RIGHT],
    pg.K_w: [Action.MOVE_UP],
    pg.K_s: [Action.MOVE_DOWN],

    pg.K_t: [Action.TOWER_1],
    pg.K_y: [Action.TOWER_2],
    pg.K_u: [Action.TOWER_3],

    pg.K_g: [Action.ORDER_1, Action.ACCEPT],
    pg.K_h: [Action.ORDER_2, Action.DECLINE],
}

BUTTONS_P2 = {
    pg.K_LEFT: [Action.MOVE_LEFT],
    pg.K_RIGHT: [Action.MOVE_RIGHT],
    pg.K_UP: [Action.MOVE_UP],
    pg.K_DOWN: [Action.MOVE_DOWN],

    pg.K_KP7: [Action.TOWER_1],
    pg.K_KP8: [Action.TOWER_2],
    pg.K_KP9: [Action.TOWER_3],

    pg.K_KP4: [Action.ORDER_1, Action.ACCEPT],
    pg.K_KP5: [Action.ORDER_2, Action.DECLINE],
}

BUTTONS_BY_PLAYER = {1: BUTTONS_P1, 2: BUTTONS_P2}
