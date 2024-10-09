# ml_agent/snake_env.py

import gym
from gym import spaces
import numpy as np
import random

class SnakeEnv(gym.Env):
    def _init_(self):
        super(SnakeEnv, self)._init_()
        
        # Define the action space and observation space
        self.action_space = spaces.Discrete(4)  # 4 actions: 0=left, 1=right, 2=up, 3=down
        
        # Observation space (the grid where the snake moves)
        # We simplify the snake game grid to a 10x10 grid (for learning purposes)
        self.grid_size = 10
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.grid_size, self.grid_size, 3), dtype=np.uint8)

        # Initialize the snake and food position
        self.snake = [(5, 5)]  # Snake starts at the center of the grid
        self.food = self._place_food()
        self.snake_direction = 2  # Start moving up

        # Snake movement directions
        self.directions = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}

        # Game state
        self.done = False
        self.score = 0

    def reset(self):
        # Reset the game state
        self.snake = [(5, 5)]
        self.food = self._place_food()
        self.snake_direction = 2
        self.done = False
        self.score = 0
        return self._get_observation()

    def step(self, action):
        # Move the snake
        self._move_snake(action)

        # Check for collisions or eating food
        if self._check_collision():
            self.done = True
            reward = -10  # Negative reward for hitting the wall or snake itself
        elif self.snake[0] == self.food:
            self.snake.append(self.snake[-1])  # Grow the snake
            self.food = self._place_food()
            reward = 10  # Positive reward for eating food
            self.score += 1
        else:
            reward = 0  # Small reward for each move

        return self._get_observation(), reward, self.done, {}

    def render(self, mode="human"):
        # Simple print rendering of the grid
        grid = np.zeros((self.grid_size, self.grid_size), dtype=np.int)
        for pos in self.snake:
            grid[pos] = 1  # Mark snake's position
        grid[self.food] = 2  # Mark food's position

        print(grid)

    def _get_observation(self):
        # Return a simple grid with snake and food positions
        grid = np.zeros((self.grid_size, self.grid_size, 3), dtype=np.uint8)
        for pos in self.snake:
            grid[pos[1], pos[0]] = [0, 255, 0]  # Green for snake
        grid[self.food[1], self.food[0]] = [255, 0, 0]  # Red for food
        return grid

    def _move_snake(self, action):
        # Update the snake's direction based on action
        if action in self.directions:
            direction = self.directions[action]
            new_head = (self.snake[0][0] + direction[0], self.snake[0][1] + direction[1])
            self.snake = [new_head] + self.snake[:-1]

    def _check_collision(self):
        # Check if the snake hit the wall or itself
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= self.grid_size or head_y < 0 or head_y >= self.grid_size:
            return True
        if len(self.snake) > 1 and self.snake[0] in self.snake[1:]:
            return True
        return False

    def _place_food(self):
        # Place food randomly on the grid
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                return (x, y)

# Register the environment
gym.register(
    id='Snake-v0',
    entry_point='ml_agent.snake_env:SnakeEnv',
)