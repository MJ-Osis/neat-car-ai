import neat
import os
import pickle

from car import Car
from track import make_track
from window import Window
from helper import Plotter

GEN = 0
best_lap = 0

win = Window(1080, 480)
track = make_track(win)

def main(genomes, config):

    global GEN
    global best_lap
    gen_winner = 0
    GEN += 1

    nets = []
    ge = []
    lap_times = []

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

            if crash or car.check_time > 50 or car.lap_count > 5:
                if len(cars) == 1:
                    run = False

                lap_times.append(car.best_lap)

                ge[x].fitness -= 1
                cars.pop(x)
                nets.pop(x)
                ge.pop(x)

    for t in lap_times:
        if t < best_lap or best_lap == 0:
            best_lap = t
        if t < gen_winner or gen_winner == 0:
            gen_winner = t

    track.reset()
    print("\nBest lap time: " + str(best_lap))
    print("Gen winner time: " + str(gen_winner) + "\n")

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

    winner = p.run(main, 100)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()

def replay_genome(config_path, genome_path="winner.pkl"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    main(genomes, config)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward_car.txt')
    run(config_path)
    #replay_genome(config_path, genome_path="winner.pkl")

