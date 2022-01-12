import matplotlib.pyplot as plt
from IPython import display

class Plotter:
    def __init__(self):
        self.plot_scores = []
        self.plot_mean_scores = []
        self.plot_rewards = []
        self.plot_mean_rewards = []

        self.total_score = 0
        self.total_rewards = 0
        self.record = 0

        plt.ion()

    def update(self, score, reward, n_games):

            print('Game', n_games, 'Score', score, 'Record:', self.record)

            self.plot_scores.append(score)
            self.plot_rewards.append(reward/10 + 10)
            self.total_score += score
            self.total_rewards += reward
            mean_score = self.total_score / n_games
            mean_reward = self.total_rewards / n_games
            self.plot_mean_scores.append(round(mean_score, 2))
            self.plot_mean_rewards.append(mean_reward/10)
            self.plot(self.plot_scores, self.plot_rewards, self.plot_mean_scores, self.plot_mean_rewards)    

    def check_record(self, score):
        if score <= self.record: return False
        self.record = score
        return True

    def plot(self, scores, rewards, mean_scores, mean_rewards):
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        plt.title('Training...')
        plt.xlabel('Number of Games')
        plt.ylabel('Score')
        plt.plot(scores, 'red')
        plt.plot(rewards, 'blue')
        plt.plot(mean_scores, 'orange')
        plt.plot(mean_rewards, 'violet')
        plt.ylim(ymin=0)
        plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
        plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
        plt.pause(0.0001)