import pygame
import math


car_img = pygame.image.load('pic/car_img.png')



class Window:
    def __init__(self, win_w, win_h):

        self.win_w = win_w
        self.win_h = win_h

        self.win = pygame.display.set_mode((win_w, win_h))

        self.clock = pygame.time.Clock()
        self.speed = 1000

    def redraw_win(self, car, track, agent):

        self.clock.tick(self.speed)

        pygame.draw.rect(self.win, (255, 255, 255), (0, 0, self.win_w, self.win_h))

        self.draw_car(car_img, car)
        self.draw_track(track)
        self.draw_track_check(track)
        self.draw_radar(car, agent, track)

        pygame.display.update()

    def draw_car(self, image, car):

        w, h = image.get_size()

        blitRotate(self.win, image, (car.x + w/2, car.y + h/2), (w/2, h/2), car.angle)

    def draw_track(self, track):
        for p, point in enumerate(track.barrier_p1):
            if p > 0:
                pygame.draw.line(self.win, (0, 0, 0), (track.barrier_p1[p-1].get_x(), track.barrier_p1[p-1].get_y()), (point.get_x(), point.get_y()), 5)

        for p, point in enumerate(track.barrier_p2):
            if p > 0:
                pygame.draw.line(self.win, (0, 0, 0), (track.barrier_p2[p-1].get_x(), track.barrier_p2[p-1].get_y()), (point.get_x(), point.get_y()), 5)

    def draw_track_check(self, track):

        for p, point in enumerate(track.checkpoints):
            pygame.draw.line(self.win, point.get_col(), (point.get_x1(), point.get_y1()), (point.get_x2(), point.get_y2()))

    def draw_radar(self, car, agent, track):

        for i in range(5):

            x = car.x + math.cos(math.radians(car.angle - 90 + i * 45)) * agent.get_state(car, track)[i]
            y = car.y - math.sin(math.radians(car.angle - 90 + i * 45)) * agent.get_state(car, track)[i]

            pygame.draw.line(self.win, (i * 50, 0, 0), (car.x + car.width/2, car.y + car.height/2), (x, y))





def blitRotate(surf, image, pos, originPos, angle):
    # calcaulate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    surf.blit(rotated_image, origin)

    # draw rectangle around the image
    pygame.draw.rect(surf, (255, 0, 0), (*origin, *rotated_image.get_size()), 2)


