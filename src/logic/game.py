from enum import Enum
from typing import Optional, List
from copy import copy

import pygame as pg

from logic import consts


class Game:
    def __init__(self):
        self.player_one: Player = Player(self, 1)
        self.player_two: Player = Player(self, 2)
        self.players: List[Player] = [self.player_one, self.player_two]

        self.spots: list[Spot] = []
        self.projectiles: list[Projectile] = []

        self.time_to_income = consts.INCOME_PERIOD
        self.time = 0

        self.controller_moves: dict[(str, Spot), Spot] = dict()

    def update(self):
        for s in self.spots:
            s.update()
        for p in self.projectiles:
            p.update()
        self.player_one.update()
        self.player_two.update()

        # income
        self.time += 1
        self.time_to_income -= 1
        if self.time_to_income == 0:
            self.income_frame()
            self.time_to_income = consts.INCOME_PERIOD

    def income_frame(self):
        self.player_one.money += consts.INCOME_BASIC
        self.player_two.money += consts.INCOME_BASIC

        for spot in self.spots:
            if spot.tower is not None:
                spot.tower.player.money += consts.INCOME_PER_TOWER
                spot.tower.income_frame()


class Spot:
    def __init__(self, game: Game):
        self.game = game
        self.pos: pg.Vector2 = pg.Vector2(0.0, 0.0)
        self.neighbours: list[Spot] = []

        self.tower: Optional[Tower] = None
        self.ban_time: int = 0
        self.banned_player: Optional[Player] = None

    def update(self):
        # player ban
        if self.banned_player is not None:
            self.ban_time -= 1
        if self.ban_time <= 0:
            self.banned_player = None

        if self.tower is not None:
            self.tower.update()

    def ask_build_tower(self, tower_type, player: 'Player', check_only=False):
        is_connected = False
        for nei in self.neighbours:
            if nei.tower is not None and nei.tower.player == player:
                is_connected = True
                break

        if self.banned_player != player \
                and player.money > tower_type.COST \
                and self.tower is None \
                and is_connected \
                and player.building_cds[tower_type] == 0:
            if check_only:
                return True
            else:
                return self.build_tower(tower_type, player)
        else:
            if check_only:
                return False
            else:
                return None

    def build_tower(self, tower_type, player: 'Player'):
        tower = self.create_tower(tower_type, player)

        player.money -= tower_type.COST
        tower.attack_cd = tower.BUILDING_TIME

        # updating player cds
        for t in player.tower_types:
            player.building_cds[t] = \
                max(consts.BUILDING_CD_SHARED, player.building_cds[t])
        player.building_cds[tower_type] = tower.BUILDING_CD

        return tower

    def create_tower(self, tower_type, player: 'Player'):
        tower: Tower = tower_type(self.game, self, player)
        self.tower = tower
        return tower


class Tower:
    def __init__(self, game: Game, spot: Spot, player: 'Player'):
        self.game = game
        self.spot: Spot = spot
        self.player: Player = player

        self.hp: int = self.MAX_HP
        self.target: Optional[Tower] = None
        self.attack_cd: int = 0

    def update(self):
        self.attack_cd -= 1
        self.attack_cd = max(0, self.attack_cd)

        self.update_target()

        if self.target is not None:
            self.try_shoot(self.target)

    def try_shoot(self, target: 'Tower'):
        if (target.spot.pos - self.spot.pos).length() < self.ATTACK_RANGE \
                and self.attack_cd == 0:
            self.shoot(target)
            return True
        else:
            return False

    def shoot(self, target: 'Tower'):
        projectile = Projectile(target, self, self.ATTACK_DAMAGE, self.PROJECTILE_SPEED)
        self.game.projectiles.append(projectile)
        self.attack_cd = self.ATTACK_CD

    def take_damage(self, dmg: int):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def ask_set_target(self, target: Optional['Tower'], check_only=False):
        if target is not None \
                and target.player != self.player \
                and (self.spot.pos - target.spot.pos).length() < self.ATTACK_RANGE:
            if not check_only:
                self.target = target
            return True
        else:
            return False

    def update_target(self):
        if self.target is not None \
                and not self.target.is_alive():
            self.target = None

        # auto attack
        if self.target is None:
            cands = list(filter(
                lambda s:
                    s.tower is not None and
                    s.tower.player != self.player and
                    (s.pos - self.spot.pos).length() < self.ATTACK_RANGE,
                self.game.spots
            ))
            # choose the most damaged target, if equal - the nearest
            cands.sort(key=lambda s: (s.pos - self.spot.pos).length())
            cands.sort(key=lambda s: s.tower.hp / s.tower.MAX_HP)
            if len(cands) > 0:
                self.ask_set_target(cands[0].tower)

    def die(self):
        spot = self.spot
        spot.tower = None
        spot.banned_player = self.player
        spot.ban_time = consts.DELAY_AFTER_TOWER_DEATH

    def is_alive(self):
        return self.hp > 0

    class OrderType(Enum):
        NONE = 0
        UNDIR = 1
        DIR = 2

    def ask_order_type(self, act: int, check_only=True):
        if act == 1:
            return Tower.OrderType.DIR
        else:
            return Tower.OrderType.NONE

    def ask_order(self, act: int, target: Optional[Spot] = None, check_only=False):
        if act == 1:
            return self.ask_set_target(target.tower, check_only=check_only)
        else:
            if check_only:
                return False
            else:
                raise ValueError(f"Unexpected number of order for standart tower: {act}")

    def income_frame(self):
        pass

    @property
    def MAX_HP(self):
        raise NotImplementedError

    @property
    def COST(self):
        raise NotImplementedError

    @property
    def ATTACK_CD(self):
        raise NotImplementedError

    @property
    def ATTACK_DAMAGE(self):
        raise NotImplementedError

    @property
    def ATTACK_RANGE(self):
        raise NotImplementedError

    @property
    def PROJECTILE_SPEED(self):
        raise NotImplementedError

    @property
    def BUILDING_TIME(self):
        raise NotImplementedError

    @property
    def BUILDING_CD(self):
        raise NotImplementedError

    @property
    def NAME(self):
        raise NotImplementedError

    ORDER_NAMES = ['Set target']


class Projectile:
    def __init__(self, target: Tower, sender: Tower, damage: int, speed: float):
        self.target = target
        self.sender = sender
        self.damage = damage
        self.speed = speed

        self.pos = copy(sender.spot.pos)
        self.target_pos = copy(target.spot.pos)
        self.effects = []
        self.game = target.game

    def collide(self):
        if self.target.hp > 0:
            self.target.take_damage(self.damage)
        self.game.projectiles.remove(self)

    def update(self):
        try:
            dir = (self.target_pos - self.pos).normalize()
            self.pos += dir * self.speed

            if (self.target_pos - self.pos).length() < consts.COLLIDE_DIST:
                self.collide()
        except ValueError:
            self.collide()


class Player:
    def __init__(self, game: Game, player_id: int):
        assert player_id == 1 or player_id == 2
        self.id = player_id
        self.game = game

        self.tower_types: list = []

        self.building_cds: dict = {}
        self.money = 0

    def set_tower_types(self, tower_types: list):
        self.tower_types = tower_types
        for tt in tower_types:
            self.building_cds[tt] = 0

    def update(self):
        for t in self.building_cds:
            if self.building_cds[t] > 0:
                self.building_cds[t] -= 1
