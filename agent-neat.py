import neat
import os
import pickle

from car import Car
from track import make_track
from window import Window
from helper import Plotter

GEN = 0
gen_winner = 0

win = Window(1080, 480)
track = make_track(win)

def main(genomes, config):

    global GEN
    global gen_winner
    GEN += 1

    nets = []
    ge = []

    cars = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car(track))
        g.fitness = 0
        ge.append(g)

    run = True
    while run:
        win.redraw_win(cars, track)

        for x, car in enumerate(cars):

            output = nets[x].activate(car.get_state(track))
            
            reward, crash, score = car.play_step(output, track)
            ge[x].fitness += reward 

            if crash or car.check_time > 50:
                if len(cars) == 1: gen_winner = x

                ge[x].fitness -= 1
                cars.pop(x)
                nets.pop(x)
                ge.pop(x)

        alive = len(cars)
        if alive <= 0: run = False

    track.reset()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 200)
    # with open("winner.pkl", "wb") as f:
    #     pickle.dump(winner, f)
    #     f.close()

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward_car.txt')
    run(config_path)

