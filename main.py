import pygame
import math
from car import Car
from window import Window
from track1 import make_track



def main():

    win = Window(1080, 480)

    race_track = make_track(win)

    car = Car(race_track.get_start_x(), race_track.get_start_y(), race_track.get_start_angle())

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            car.gas()
        else:
            car.roll()

        if keys[pygame.K_a]:
            car.angle += 5

        if keys[pygame.K_d]:
            car.angle -= 5

        if keys[pygame.K_SPACE]:
            car.brake()

        if car.collide(race_track):
            print('collide')

        if car.get_check(race_track) == 1:
            print('check')
        elif car.get_check(race_track) == 2:
            print('start')

        car.move()

        win.redraw_win(car, race_track)

main()







