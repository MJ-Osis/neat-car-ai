import pygame
import math
from window import Window
from help import Point
from help import Checkpoint



class Track:

    def __init__(self):

        self.barrier_p1 = []
        self.barrier_p2 = []

        self.collision_p1 = []
        self.collision_p2 = []

        self.checkpoints = []

        self.barriers = 2

        self.e = False
        self.construct = True

    def end(self):
        self.barriers -= 1

        if self.barriers == 1:
            self.barrier_p1.append(self.barrier_p1[0])

        else:
            self.barrier_p2.append(self.barrier_p2[0])

            self.make_col_1(1)
            self.make_col_2(1)
            self.make_checkpoints(50)

            self.e = True


    def save_p(self, x_p, y_p):

        if self.barriers == 2:
            if len(self.barrier_p1) == 0:
                self.barrier_p1.append(Point(x_p, y_p))

                print(self.barrier_p1)

            else:
                if abs(x_p - self.barrier_p1[0].get_x()) < 10 and abs(y_p - self.barrier_p1[0].get_y()) < 10:
                    self.end()

                else:
                    self.barrier_p1.append(Point(x_p, y_p))

        else:
            if len(self.barrier_p2) == 0:
                self.barrier_p2.append(Point(x_p, y_p))

            else:
                if abs(x_p - self.barrier_p2[0].get_x()) < 10 and abs(y_p - self.barrier_p2[0].get_y()) < 10:
                    self.construct = False
                    self.end()

                else:
                    self.barrier_p2.append(Point(x_p, y_p))


    def draw(self, win):

        pygame.draw.rect(win.win, (255, 255, 255), (0, 0, 1080, 480))

        if self.construct:
            if self.barriers == 2 and len(self.barrier_p1) != 0:
                pygame.draw.circle(win.win, (50, 200, 0), (self.barrier_p1[0].get()), 10)
            elif self.barriers == 1:
                if len(self.barrier_p2) == 0:
                    pygame.draw.circle(win.win, (200, 50, 0), (self.barrier_p1[0].get()), 50)
                else:
                    pygame.draw.circle(win.win, (50, 200, 0), (self.barrier_p2[0].get()), 10)


        for p, cords in enumerate(self.barrier_p1):
            if p > 0:
                pygame.draw.line(win.win, (0, 0, 0), (self.barrier_p1[p-1].get()), (self.barrier_p1[p].get()), 5)

        for p, cords in enumerate(self.barrier_p2):
            if p > 0:
                pygame.draw.line(win.win, (0, 0, 0), (self.barrier_p2[p-1].get()), (self.barrier_p2[p].get()), 5)

        pygame.display.update()

    def make_col_1(self, delay):

        for p, point in enumerate(self.barrier_p1):
            if p + 1 != len(self.barrier_p1):
                length = math.sqrt(((self.barrier_p1[p+1].get_x() - point.get_x()) ** 2) + ((self.barrier_p1[p+1].get_y() - point.get_y()) ** 2))
                lengthx = self.barrier_p1[p+1].get_x() - point.get_x()
                lengthy = self.barrier_p1[p+1].get_y() - point.get_y()
                for i in range(math.ceil(length / delay)):
                    offsetx = (delay * lengthx) / length
                    offsety = (delay * lengthy) / length

                    self.collision_p1.append(Point(point.get_x() + i * offsetx, point.get_y() + i * offsety))

    def make_col_2(self, delay):

        for p, point in enumerate(self.barrier_p2):
            if p + 1 != len(self.barrier_p2):
                length = math.sqrt(((self.barrier_p2[p+1].get_x() - point.get_x()) ** 2) + ((self.barrier_p2[p+1].get_y() - point.get_y()) ** 2))
                lengthx = self.barrier_p2[p + 1].get_x() - point.get_x()
                lengthy = self.barrier_p2[p + 1].get_y() - point.get_y()
                for i in range(math.ceil(length / delay)):
                    offsetx = (delay * lengthx) / length
                    offsety = (delay * lengthy) / length

                    self.collision_p2.append(Point(point.get_x() + i * offsetx, point.get_y() + i * offsety))

    def make_checkpoints(self, checks):

        x1points = []
        y1points = []
        x2points = []
        y2points = []

        every1 = round(len(self.collision_p1) / checks)
        every2 = round(len(self.collision_p2) / checks)

        self.checkpoints.append(Checkpoint(self.barrier_p1[0].get_x(),
                                           self.barrier_p1[0].get_y(),
                                           self.barrier_p2[0].get_x(),
                                           self.barrier_p2[0].get_y(),
                                           col=(0, 0, 200), start=True))

        for p, point in enumerate(self.collision_p1):
            if p % every1 == 0 and p != 0:
                x1points.append(point.get_x())
                y1points.append(point.get_y())

        for p, point in enumerate(self.collision_p2):
            if p % every2 == 0 and p != 0:
                x2points.append(point.get_x())
                y2points.append(point.get_y())

        for p, point in enumerate(x1points):
            if p < len(x2points):
                self.checkpoints.append(Checkpoint(point, y1points[p], x2points[p], y2points[p]))

    def get_start_x(self):

        start_x = (self.barrier_p1[0].get_x() + self.barrier_p2[0].get_x()) / 2

        return start_x


    def get_start_y(self):

        start_y = (self.barrier_p1[0].get_y() + self.barrier_p2[0].get_y()) / 2

        return start_y

    def get_start_angle(self):

        xm = self.barrier_p2[0].get_x() - self.barrier_p1[0].get_x()
        ym = self.barrier_p2[0].get_y() - self.barrier_p1[0].get_y()

        if xm == 0: slope = 0 
        else: slope = ym/xm

        alpha = math.degrees(math.atan(slope))

        if alpha >= 0:
            beta = 90 - alpha
        else:
            beta = 270 - alpha

        return beta

    def reset(self):

        for p, point in enumerate(self.checkpoints):

            if p != 0:
                point.set_col((0, 200, 0))






def make_track(win):

    run = True

    race_track = Track()

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if race_track.barriers == 2:
                    if len(race_track.barrier_p1) < 0:
                        if abs(event.pos[0] - race_track.barrier_p1[-1].get_x()) > 5 and abs(event.pos[1] - race_track.barrier_p1[-1].get_y()) > 5:
                            race_track.save_p(event.pos[0], event.pos[1])

                    else:
                        race_track.save_p(event.pos[0], event.pos[1])
                else:
                    if len(race_track.barrier_p2) > 0:
                        if abs(event.pos[0] - race_track.barrier_p2[-1].get_x()) > 5 and abs(event.pos[1] - race_track.barrier_p2[-1].get_y()) > 5:
                            race_track.save_p(event.pos[0], event.pos[1])

                    else:
                        race_track.save_p(event.pos[0], event.pos[1])

        if race_track.e == True:
                run = False


        race_track.draw(win)

    return race_track




