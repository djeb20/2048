import numpy as np
import matplotlib.pyplot as plt
"""
Environment class for 2048
"""

# I HAVE NOT ACCOUNTED FOR MULTIPLE ABSORBS IN ONE GO! BACKWARDS?

class env_2048:

    def __init__(self):

        self.num_actions = 4
        self.state_dim = 16

    def reset(self):

        self.grid = np.zeros((4, 4))
        self.add_number()
        self.add_number()

        return self.grid.flatten()

    def step(self, action):
        """
        Step in the environment, 4 available actions: up, right, down, left.
        """

        done = False # Assume not done

        grid = np.rot90(self.grid, action, (1, 0)) # Rotate to have gravity facing up
        grid, reward = self.take_action(grid)
        self.grid = np.rot90(grid, action) # Rotate back

        if (grid == self.grid).all(): reward -= 1 # Punish for taking pointless action
        else: self.add_number() # Add new number, only when move made

        if (self.grid == 0).sum() == 0: # Game might have ended
            done = True # Assume game has ended
            for a in range(4): # Try all actions
                if (np.rot90(self.take_action(np.rot90(self.grid, a, (1, 0))[0]), a) != self.grid).any(): # If action causes change

                    done = False
                    break

        return self.grid.flatten(), reward, done, False

    def take_action(self, grid):
        """
        Tries to take an action in a grid
        """

        # First loop through and push everything in the correct blank square
        for i in range(2, -1, -1):

            zero_index = grid[i] == 0
            grid[i:][:, zero_index] = np.append(grid[i+1:][:, zero_index], np.zeros((1, zero_index.sum())), axis=0)

        # Now, assuming there is no falling, add the tiles
        reward = 0
        for i in range(3):

            same_index = grid[i] == grid[i+1]

            grid[i][same_index] += grid[i+1][same_index]
            reward += grid[i][same_index].sum()
            grid[i+1:][:, same_index] = np.append(grid[i+2:][:, same_index], np.zeros((1, same_index.sum())), axis=0)

        return grid, reward


    def add_number(self):
        """
        Takes a grid and adds a 2 randomly with prob 0.8 and 4 with prob 0.2
        """

        row_index, col_index = np.where(self.grid == 0)
        index = np.random.randint(len(row_index))
        self.grid[row_index[index], col_index[index]] = np.random.choice([2, 4], p=[0.8, 0.2])

    def render(self):
        """
        Renders the environment.
        """

        print(self.grid)