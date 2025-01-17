import math


def get_distance(x1, y1, x2, y2):
    """calculates the distance between 2 objects"""
    distance = math.sqrt((math.pow(x1 - x2, 2)) +
                         (math.pow(y1 - y2, 2)))

    return distance
