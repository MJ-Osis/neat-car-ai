import math
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = round(x)
        self.y = round(y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get(self):
        return self.x, self.y

    def set(self, x, y):
        self.x = x
        self.y = y


class Checkpoint:

    def __init__(self, x1, y1, x2, y2, col=(0, 200, 0), start=False):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.col = col
        self.start = start

    def get(self):
        return self.x1, self.y1, self.x2, self.y2

    def get_x1(self):
        return self.x1

    def get_y1(self):
        return self.y1

    def get_x2(self):
        return self.x2

    def get_y2(self):
        return self.y2

    def set(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def set_col(self, col):
        self.col = col

    def get_col(self):
        return self.col

    def get_start(self):
        return self.start


def get_points(delay, x1, y1, x2, y2):
    points = []

    lengthx = x2 - x1
    lengthy = y2 - y1
    length = math.sqrt((lengthx ** 2) + (lengthy ** 2))

    for i in range(math.ceil(length / delay)):
        offsetx = (delay * lengthx) / length
        offsety = (delay * lengthy) / length

        points.append(Point(x1 + i * offsetx, y1 + i * offsety))

    return points

def give_length(ang, car, track):
    a = math.radians(ang)

    p1, p2 = make_radar(a, car, 200)

    if not find_seg1(a, track, car):
        return 200

    p3, p4 = find_seg1(a, track, car)

    if not line_intersection(p1, p2, p3, p4):
        return 200

    else:
        length = line_intersection(p1, p2, p3, p4)

    return round(length)


def find_seg(ang, track, car):

    p1, p2 = make_radar(ang, car, 200)

    plausible = []
    plaus = 0

    lent = 1000

    for pa, pointa in enumerate(track.barrier_p1):

        if intersect(p1, p2, track.barrier_p1[pa - 1], pointa):
            pointsa = track.barrier_p1[pa - 1], pointa
            plausible.append(pointsa)

    for pb, pointb in enumerate(track.barrier_p2):

        if intersect(p1, p2, track.barrier_p2[pb - 1], pointb):
            pointsb = track.barrier_p2[pb - 1], pointb
            plausible.append(pointsb)

    if plausible:
        for i, pon in enumerate(plausible):
            len1 = math.sqrt(((pon[0].x - p1.x) ** 2) + ((pon[0].y - p1.y) ** 2))
            len2 = math.sqrt(((pon[1].x - p1.x) ** 2) + ((pon[1].y - p1.y) ** 2))
            len3 = (len1 + len2) / 2

            if len3 < lent:
                lent = len3
                plaus = i

    else:
        return False

    return plausible[plaus]


def find_seg1(ang, track, car):

    p1, p2 = make_radar(ang, car, 200)

    plausible = []
    plaus = 0

    lent = 1000

    for pa, pointa in enumerate(track.barrier_p1):

        if intersect(p1, p2, track.barrier_p1[pa - 1], pointa):
            pointsa = track.barrier_p1[pa - 1], pointa
            plausible.append(pointsa)

    for pb, pointb in enumerate(track.barrier_p2):

        if intersect(p1, p2, track.barrier_p2[pb - 1], pointb):
            pointsb = track.barrier_p2[pb - 1], pointb
            plausible.append(pointsb)

    if plausible:
        for i, pon in enumerate(plausible):

            poin = np.array([p1.x, p1.y])
            lin = [np.array([pon[0].x, pon[0].y]), np.array([pon[1].x, pon[1].y])]

            length = point_to_line_dist(poin, lin)

            if length < lent:
                lent = length
                plaus = i


    else:
        return False

    return plausible[plaus]




def line_intersection(point1, point2, point3, point4):
    line1 = [[point1.get_x(), point1.get_y()], [point2.get_x(), point2.get_y()]]
    line2 = [[point3.get_x(), point3.get_y()], [point4.get_x(), point4.get_y()]]

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    line_a = (point1.get_x() - x) ** 2
    line_b = (point1.get_y() - y) ** 2

    length = math.sqrt(line_a + line_b)

    return length


def make_radar(ang, car, radius):
    first = Point(car.x + car.width / 2, car.y + car.height / 2)

    second = Point(first.get_x() + math.cos(ang) * radius, first.get_y() - math.sin(ang) * radius)

    return first, second


def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def point_to_line_dist(point, line):
    """Calculate the distance between a point and a line segment.

    To calculate the closest distance to a line segment, we first need to check
    if the point projects onto the line segment.  If it does, then we calculate
    the orthogonal distance from the point to the line.
    If the point does not project to the line segment, we calculate the
    distance to both endpoints and take the shortest distance.

    :param point: Numpy array of form [x,y], describing the point.
    :type point: numpy.core.multiarray.ndarray
    :param line: list of endpoint arrays of form [P1, P2]
    :type line: list of numpy.core.multiarray.ndarray
    :return: The minimum distance to a point.
    :rtype: float
    """
    # unit vector
    unit_line = line[1] - line[0]
    norm_unit_line = unit_line / np.linalg.norm(unit_line)

    # compute the perpendicular distance to the theoretical infinite line
    segment_dist = (
        np.linalg.norm(np.cross(line[1] - line[0], line[0] - point)) /
        np.linalg.norm(unit_line)
    )

    diff = (
        (norm_unit_line[0] * (point[0] - line[0][0])) +
        (norm_unit_line[1] * (point[1] - line[0][1]))
    )

    x_seg = (norm_unit_line[0] * diff) + line[0][0]
    y_seg = (norm_unit_line[1] * diff) + line[0][1]

    endpoint_dist = min(
        np.linalg.norm(line[0] - point),
        np.linalg.norm(line[1] - point)
    )

    # decide if the intersection point falls on the line segment
    lp1_x = line[0][0]  # line point 1 x
    lp1_y = line[0][1]  # line point 1 y
    lp2_x = line[1][0]  # line point 2 x
    lp2_y = line[1][1]  # line point 2 y
    is_betw_x = lp1_x <= x_seg <= lp2_x or lp2_x <= x_seg <= lp1_x
    is_betw_y = lp1_y <= y_seg <= lp2_y or lp2_y <= y_seg <= lp1_y
    if is_betw_x and is_betw_y:
        return segment_dist
    else:
        # if not, then return the minimum distance to the segment endpoints
        return endpoint_dist
