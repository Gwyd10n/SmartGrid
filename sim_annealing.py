from copy import deepcopy
from random import shuffle
import numpy as np
import math


def sim_ann(grid, n_alg, cooling='linear', Ts=10, Te=1, d=1):
    accept = 0
    i = 0
    cooling_schemes = {'linear': Ts - i * (Ts - Te) / n_alg, 'exponential': Ts * math.pow(Te / Ts, i / n_alg),
                       'sigmoidal': Te + (Ts - Te) / (1 + np.exp(0.3 * (i - n_alg / 2))), 'geman&geman': Ts / (np.log(i + d))}

    for i in range(n_alg):
        score = grid.tot_len()
        # prob_grid = swap_one(grid)
        # score_new = prob_grid.get_cost()
        cables = grid.get_cables()
        batteries = grid.get_batteries()
        houses = grid.get_houses()
        # Get keys from the cable dictionary
        us_ckeys = list(cables.keys())
        ckeys = []

        for bkey in batteries:
            group = []
            for ckey in us_ckeys:
                if cables[ckey].get_batt() == bkey:
                    group.append(ckey)
            ckeys.append(group)

        shuffle(ckeys)
        shuffle(ckeys[0])
        shuffle(ckeys[1])

        orgA = cables[ckeys[0][0]]
        orgB = cables[ckeys[1][0]]
        newA = deepcopy(orgA)
        newB = deepcopy(orgB)

        houseA = houses[orgA.get_id()]
        houseB = houses[orgB.get_id()]

        battA = batteries[orgA.get_batt()]
        battB = batteries[orgB.get_batt()]

        newA.change_route(houseA.get_coord(), battB.get_coord())
        newA.add_batt(battB.get_id())
        newB.change_route(houseB.get_coord(), battA.get_coord())
        newB.add_batt(battA.get_id())

        score_new = score - (orgA.get_length() + orgB.get_length()) + (newA.get_length() + newB.get_length())

        if battA.get_cap() > houseB.get_max() and battB.get_cap() > houseA.get_max():

            if score >= score_new:
                accept = 1

            elif score < score_new:
                accept = max(0, min(1, np.exp(-(score_new - score) / T)))
        else:
            accept = 0

        T = cooling_schemes[cooling]
        print(f'Iteration: {i}, Accepted score: {score}, Current score: {score_new}, Temp: {T}')
        if np.random.rand() < accept:
            grid.rem_cable(orgA.get_id())
            grid.rem_cable(orgB.get_id())
            grid.add_cable(newA)
            grid.add_cable(newB)
    return grid
