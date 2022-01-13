import pygame
import math
import numpy as np
from help import Point
from help import get_points, give_length

car_img = pygame.image.load('pic/car_img.png')


class Car:
    def __init__(self, track):

        self.reset(track)

        self.acc = 5

        self.width = 20
        self.height = 10

        self.img = car_img

    def act(self, action):

        wheel = action[0]
        motor = [action[1], action[2]]

        self.steer(wheel)

        if motor[0] > 0:
            self.gas()
        elif motor[1] > 0:
            self.brake()
        else:
            self.roll()

        self.move()


    def act1(self, action):

        if np.array_equal(action, [1, 0, 0, 0, 0, 0, 0]):
            self.gas()
        elif np.array_equal(action, [0, 1, 0, 0, 0, 0, 0]):
            self.gas()
            self.go_right()
        elif np.array_equal(action, [0, 0, 1, 0, 0, 0, 0]):
            self.gas()
            self.go_left()
        elif np.array_equal(action, [0, 0, 0, 1, 0, 0, 0]):
            self.brake()
        elif np.array_equal(action, [0, 0, 0, 0, 1, 0, 0]):
            self.roll()
        elif np.array_equal(action, [0, 0, 0, 0, 0, 1, 0]):
            self.roll()
            self.go_right()
        else:
            self.roll()
            self.go_right()

        self.move()


    def move(self):
        self.a = math.radians(self.angle)
        self.x += math.cos(self.a) * self.vel
        self.y -= math.sin(self.a) * self.vel
        
    def gas(self):
        if self.vel > 200: return
        if self.vel < 5: self.vel += 1
        self.vel *= 1.01

    def brake(self):
        if self.vel < 1:
            self.vel = 0
        else:
            self.vel = self.vel * 0.95

    def roll(self):
        if self.vel > 0:
            self.vel -= self.vel * 0.05
        else:
            self.vel = 0

    def go_right(self):
        self.angle -= 1 

    def go_left(self):
        self.angle += 1

    def straight(self):
        self.angle = self.angle

    def steer(self, v):
        self.angle += v * 5


    def get_check1(self, track):

        mask = pygame.mask.from_surface(self.img)

        (width, height) = mask.get_size()

        for n, pon in enumerate(track.checkpoints):

            if n == self.gotten or self.gotten % 50 == n:

                points = get_points(1,
                                    track.checkpoints[n].get_x1(),
                                    track.checkpoints[n].get_y1(),
                                    track.checkpoints[n].get_x2(),
                                    track.checkpoints[n].get_y2())

                for p, point in enumerate(points):

                    if int(self.x) <= point.get_x() <= int(self.x + width):
                        if int(self.y) <= point.get_y() <= int(self.y + height):
                            if pon.get_start():
                                for pon in track.checkpoints:
                                    pon.set_col((0, 200, 0))
                                self.gotten += 1
                                return 2
                            else:
                                pon.set_col((200, 0, 0))
                                self.gotten += 1
                                return 1

        return 0


    def get_check(self, track):

        mask = pygame.mask.from_surface(self.img)

        (width, height) = mask.get_size()

        for n, pon in enumerate(track.checkpoints):

            if (pon.get_col() == (0, 200, 0) or (0, 0, 200)) and (
                    track.checkpoints[n - 1].get_col() == (200, 0, 0) or track.checkpoints[n - 1].get_col() == (
                    0, 0, 200)) or track.checkpoints[19].get_col == (200, 0, 0):

                points = get_points(1,
                                    track.checkpoints[n].get_x1(),
                                    track.checkpoints[n].get_y1(),
                                    track.checkpoints[n].get_x2(),
                                    track.checkpoints[n].get_y2())

                for p, point in enumerate(points):

                    if int(self.x) <= point.get_x() <= int(self.x + width):
                        if int(self.y) <= point.get_y() <= int(self.y + height):
                            if pon.get_start():
                                return 2
                            else:
                                pon.set_col((200, 0, 0))
                                return 1

        return 0

    def collide(self, track):

        mask = pygame.mask.from_surface(self.img)

        (width, height) = mask.get_size()

        for p, point in enumerate(track.collision_p1):

            if int(self.x) <= point.get_x() <= int(self.x + width):
                if int(self.y) <= point.get_y() <= int(self.y + height):
                    return True

        for p, point in enumerate(track.collision_p2):

            if int(self.x) <= point.get_x() <= int(self.x + width):
                if int(self.y) <= point.get_y() <= int(self.y + height):
                    return True

        return False

    def play_step(self, action, track):

        self.lap_time += 1
        self.check_time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.act(action)

        reward = 1
        game_over = False

        if self.collide(track) or self.check_time > 500:
            game_over = True
            reward = 0

        c = self.get_check1(track)

        if c == 0: return reward, game_over, self.score
            
        elif c == 2:
            reward = int(500 / self.lap_time) + 50
            self.score += int(100 / self.lap_time)
            if self.lap_time < self.best_lap or self.best_lap == 0:
                self.best_lap = self.lap_time
            self.lap_time = 0
            self.lap_count += 1
            print("Lap completed, best lap: " + str(self.best_lap))

        elif c == 1:
            reward = 10
            self.score += 1
            self.check_time = 0

        return reward, game_over, self.score

        

    def get_state(self, track):

        state1 = []

        for i in range(5):
            ang = self.angle - 90 + i * 45

            state1.append(give_length(ang, self, track))

        state2 = [self.x, self.y, self.vel]

        state = state1 + state2

        return np.array(state, dtype=int)

    def reset(self, track):

        self.x = track.get_start_x()
        self.y = track.get_start_y()

        self.angle = track.get_start_angle()
        self.vel = 0

        self.lap_time = 0
        self.check_time = 0
        self.stag = 0
        self.score = 0

        self.gotten = 1

        self.best_lap = 0
        self.lap_count = 0
