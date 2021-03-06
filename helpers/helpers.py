#!/usr/bin/env python
# Gwydion Oostvogel, Sophie Schubert
"""
Helper functions for smart grid.
"""

import csv
import os


def get_man(coord_start, coord_end):
    """
    Calculate manhattan distance
    :param coord_start: tuple
    :param coord_end: tuple
    :return: int
    """

    return abs(coord_start[0] - coord_end[0]) + abs(coord_start[1] - coord_end[1])


def distance(grid):
    """
    A list with all the distances from houses to batteries
    :param grid: grid
    :return: list
    """
    houses = grid.get_houses()
    batteries = grid.get_batteries()

    distance_list = []

    # Iterate over houses
    for hkey in houses:
        distances = []
        for bkey in batteries:
            # Get manhatten distances
            dist = get_man(houses[hkey].get_coord(), batteries[bkey].get_coord())
            distances.append(dist)
        distance_list.append(distances)

    return distance_list


def lower_bound(list):
    """
    Calculates the lower bound in length units
    :param list: list
    :return: int
    """
    low = 0
    for i in range(len(list)):
        low += (min(list[i]))

    return low


def upper_bound(list):
    """
    Calculates the upper bound by looping through the houses and
    calculates the maximum length of cables in length units.
    :param list: list
    :return: int
    """
    upp = 0
    for i in range(len(list)):
        upp += (max(list[i]))

    return upp


def move(grid, list):
    """
    Moves batteries according to specific new location on the grid
    :param grid: object
    :param list: list
    :return: none
    """
    batteries = grid.get_batteries()

    # For each battery, set the new coordinates
    for indx, bkey in enumerate(batteries):
        batteries[bkey].set_coord(list[indx][0], list[indx][1])


def save_csv(grid, distr, alg):
    """
    Saves grid to CSV file.
    :param grid: object
    :param distr: int
    :param alg: string
    :return: string
    """
    houses = grid.get_houses()
    batteries = grid.get_batteries()
    cables = grid.get_cables()
    path = os.path.dirname(__file__).replace("helpers", f"data\\results\\District_{distr}_{alg}.csv")
    rows = []

    rows.append([distr, alg, grid.tot_len(), grid.get_cost()])
    for bkey in batteries:
        battery = batteries[bkey]
        rows.append([battery.get_id(), battery.get_coord()[0], battery.get_coord()[1], battery.get_cap(), battery.get_type()])
        for ckey in cables:
            if battery.get_id() == cables[ckey].get_batt():
                house = houses[ckey]
                rows.append([house.get_id(), house.get_coord()[0], house.get_coord()[1]])
                for point in cables[ckey].get_route():
                    rows.append(point)

    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    csvfile.close()
    return path
