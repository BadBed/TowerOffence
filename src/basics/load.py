import pygame as pg

from logic.game import Game, Spot
from logic.towers import BaseTower


def load_from_file(filename):
    game = Game()
    with open(filename) as f:
        def read():
            while True:
                line = f.readline()
                if line[0] != "#":
                    return line

        # Number of points
        n = int(read())

        # Spots positions
        for _ in range(n):
            spot = Spot(game)
            spot.pos = pg.Vector2(*map(float, read().split()))
            game.spots.append(spot)

        # Spots graph
        m = int(read())
        gp = game.spots
        for _ in range(m):
            i, j = tuple(map(int, read().split()))
            gp[i].neighbours.append(gp[j])
            gp[j].neighbours.append(gp[i])

        # Spots moves map
        for i in range(n):
            l, r, u, d = map(int, read().split())
            game.controller_moves[('L', gp[i])] = gp[l]
            game.controller_moves[('R', gp[i])] = gp[r]
            game.controller_moves[('U', gp[i])] = gp[u]
            game.controller_moves[('D', gp[i])] = gp[d]

        # Base towers
        b1, b2 = map(int, read().split())
        gp[b1].create_tower(BaseTower, game.player_one)
        gp[b2].create_tower(BaseTower, game.player_two)
    return game
