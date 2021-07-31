from logic.game import Tower
from logic import consts


# TODO: lose if die
# TODO: provide electricity
class BaseTower(Tower):
    MAX_HP = 6000
    COST = 700
    ATTACK_CD = 20
    ATTACK_DAMAGE = 100
    ATTACK_RANGE = consts.RANGE_SHORT
    PROJECTILE_SPEED = 8.0
    BUILDING_CD = 420
    BUILDING_TIME = 0


class MiningTower(Tower):
    # doesn't shoot
    def try_shoot(self, target: Tower):
        return False

    def update_target(self):
        pass

    def shoot(self, target: Tower):
        raise NotImplementedError

    # gives money
    def income_frame(self):
        self.player.money += self.INCOME

    MAX_HP = 3000
    COST = 300
    BUILDING_TIME = 0
    BUILDING_CD = 1800

    INCOME = 10

    ATTACK_CD = None
    ATTACK_DAMAGE = None
    ATTACK_RANGE = None
    PROJECTILE_SPEED = None


class LongRangeTower(Tower):
    MAX_HP = 3000
    COST = 200
    ATTACK_CD = 20
    ATTACK_DAMAGE = 100
    ATTACK_RANGE = consts.RANGE_LONG
    PROJECTILE_SPEED = 4.0
    BUILDING_TIME = 0
    BUILDING_CD = 420


class ShortRangeTower(Tower):
    MAX_HP = 4000
    COST = 300
    ATTACK_CD = 40
    ATTACK_DAMAGE = 300
    ATTACK_RANGE = consts.RANGE_SHORT
    PROJECTILE_SPEED = 4.0
    BUILDING_TIME = 0
    BUILDING_CD = 420
