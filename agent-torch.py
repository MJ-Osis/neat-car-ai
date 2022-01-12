import torch
import random
import numpy as np
from collections import deque
from car import Car
from track import make_track
from window import Window
from model import Linear_QNet, QTrainer
from helper import Plotter
from help import give_length

MAX_MEMORY = 1000000
BATCH_SIZE = 100
LR = 0.00001
SHOW_EVERY = 5


class Agent:

    def __init__(self):
        self.n_games = 0
        self.show_every = 10

        self.epsilon = 0.5  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(5, 256, 7)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, car, track):

        state1 = []

        for i in range(5):
            ang = car.angle - 90 + i * 45

            state1.append(give_length(ang, car, track))

        state2 = [car.x, car.y, car.vel]

        state = state1 + state2

        return np.array(state1, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation

        steer_move = [0, 0, 0]
        motor_move = [0, 0, 0]

        if random.random() < self.epsilon:
            move1 = random.randint(0, 2)
            steer_move[move1] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction1 = self.model(state0)
            pre1 = [prediction1[0], prediction1[1], prediction1[2]]
            pre2 = torch.tensor(pre1, dtype=torch.float)
            move = torch.argmax(pre2).item()
            steer_move[move] = 1

        if random.random() < self.epsilon:
            move2 = random.randint(0, 2)
            motor_move[move2] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction2 = self.model(state0)
            pre3 = [prediction2[3], prediction2[4], prediction2[5]]
            pre4 = torch.tensor(pre3, dtype=torch.float)
            move2 = torch.argmax(pre4).item()
            motor_move[move2] = 1

        final_move = steer_move + motor_move

        return final_move

    def get_action1(self, state):
        # random moves: tradeoff exploration / exploitation

        move = [0, 0, 0, 0, 0, 0, 0]

        if random.random() < self.epsilon:
            move1 = random.randint(0, 4)
            move[move1] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction1 = self.model(state0)
            pre2 = prediction1.clone().detach()
            move1 = torch.argmax(pre2).item()
            move[move1] = 1

        return move

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon
        print("Epsilon: " + str(epsilon))


def train():

    win = Window(1080, 480)

    track = make_track(win)

    agent = Agent()
    car = Car(track)

    plotter = Plotter()

    reward = 0

    while True:

        state_old = agent.get_state(car, track)

        final_move = agent.get_action1(state_old)

        rew, done, score = car.play_step(final_move, track)

        state_new = agent.get_state(car, track)

        agent.train_short_memory(state_old, final_move, rew, state_new, done)

        agent.remember(state_old, final_move, rew, state_new, done)

        #if agent.n_games % agent.show_every == 0:
        win.redraw_win(car, track, agent)

        reward += rew

        if done:

            track.reset()
            car.reset(track)

            agent.n_games += 1
            agent.train_long_memory()

            if plotter.check_record(score):
                agent.model.save()

            agent.set_epsilon(5/plotter.record)

            plotter.update(score, reward, agent.n_games)

            reward = 0


if __name__ == '__main__':
    train()
