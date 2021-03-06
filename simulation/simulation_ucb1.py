import numpy as np
import sys
sys.path.append("..")
from striatum.storage import history
from striatum.storage import model
from striatum.bandit import ucb1


class Ucb1LinearPayoff:
    def __init__(self, t, d, actions):
        self.t = t
        self.d = d
        self.actions = actions

    def data_simulation(self):
        context = np.random.uniform(0, 1, (self.t, self.d))
        desired_action = np.zeros(shape=(self.t, 1))
        n_actions = len(self.actions)
        for t in range(self.t):
            for i in range(n_actions):
                if i * self.d/n_actions < sum(context[t, :]) <= (i+1) * self.d/n_actions:
                    desired_action[t] = self.actions[i]
        return context, desired_action

    def policy_evaluation(self, policy, desired_action):
        if policy != 'UCB1':
            print("We don't support other bandit algorithms now!")
        else:
            historystorage = history.MemoryHistoryStorage()
            modelstorage = model.MemoryModelStorage()
            sum_error = 0
            policy = ucb1.UCB1(self.actions, historystorage, modelstorage)
            for t in range(self.t):
                history_id, action = policy.get_action(context=None)
                if desired_action[t][0] != action:
                    policy.reward(history_id, 0)
                    sum_error += 1
                else:
                    policy.reward(history_id, 1)
            return self.t - sum_error


if __name__ == '__main__':
    simulation = Ucb1LinearPayoff(1000, 5, [1, 2, 3, 4, 5])
    print(simulation.policy_evaluation('UCB1', simulation.data_simulation()[1])/1000.0)
