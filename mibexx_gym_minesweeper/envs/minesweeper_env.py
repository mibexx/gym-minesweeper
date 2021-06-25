import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

GAME_SIZE = 9
NUM_MINES = 10


class MinesweeperEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, game_size_x=GAME_SIZE, game_size_y=GAME_SIZE, num_mines=NUM_MINES):
        self.game_size_x = game_size_x
        self.game_size_y = game_size_y
        self.num_mines = num_mines
        self.observation_space = spaces.Box(low=-2, high=8, shape=(self.game_size_y, self.game_size_x), dtype=np.int)
        self.action_space = spaces.MultiDiscrete([self.game_size_y, self.game_size_x])
        self.state = np.zeros(shape=(self.game_size_y, self.game_size_x), dtype=np.int)
        self.mines = np.zeros(shape=(self.num_mines, 2), dtype=np.int)

    def step(self, action):
        reward = 0
        done = False

        y, x = action
        field_value = self.state[y][x]

        field_pos = np.array([[y], [x]])
        field_pos = np.ravel_multi_index(field_pos, dims=(self.game_size_y, self.game_size_x))

        if len(np.where(self.mines == field_pos)[0]) > 0:
            reward = -10
            self.state[y][x] = -2
            done = True
        elif field_value == -1:
            reward = -1
        else:
            reward = 1
            self._compute_action(action)

        unique, counts = np.unique(self.state, return_counts=True)
        state_counts = dict(zip(unique, counts))
        if state_counts[0] == self.num_mines:
            reward = 10
            done = True

        return self.state, reward, done, {}

    def _compute_action(self, action):
        fy, fx = action

        self.state[fy][fx] = -1
        field_value = 0
        for y in range(fy-1, fy+2):
            for x in range(fx-1, fx+2):
                if y < 0 or y >= self.game_size_y or x < 0 or x >= self.game_size_x:
                    continue

                field_pos = np.array([[y], [x]])
                field_pos = np.ravel_multi_index(field_pos, dims=(self.game_size_y, self.game_size_x))

                if len(np.where(self.mines == field_pos)[0]) > 0:
                    field_value += 1

        if field_value > 0:
            self.state[fy][fx] = field_value
        else:
            for y in range(fy-1, fy+2):
                for x in range(fx-1, fx+2):
                    if y < 0 or y >= self.game_size_y or x < 0 or x >= self.game_size_x:
                        continue
                    if self.state[y][x] == 0:
                        self._compute_action((y, x))

    def reset(self):
        self.state = np.zeros(shape=(self.game_size_y, self.game_size_x), dtype=np.int)
        mines = np.random.choice(self.game_size_y * self.game_size_x, size=self.num_mines, replace=False)
        self.mines = mines

        return self.state

    def render(self, mode='human'):
        print(self.state)
