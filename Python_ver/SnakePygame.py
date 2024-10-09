# SnakePygame.py

import pygame
from SnakeQAgent import SnakeQAgent
from LearnSnake import LearnSnake
import numpy as np
import pickle

class SnakeGameVisualizer:
    def __init__(self, q_table):
        self.q_table = q_table
        self.env = LearnSnake()
        self.screen_width = self.env.screen_width
        self.screen_height = self.env.screen_height
        self.snake_size = self.env.snake_size
        self.game_over = False

    def draw_elements(self):
        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

            # Get the current state
            state = self.env.get_state()
            action = np.argmax(self.q_table[state])  # Choose the best action based on Q-table
            new_state, reward, self.env.game_close = self.env.step(action)

            # Draw the game elements
            screen.fill((0, 0, 0))  # Clear the screen

            # Draw the snake
            for r, c in self.env.snake_coords:
                pygame.draw.rect(screen, (0, 255, 0), [c * self.snake_size, r * self.snake_size, self.snake_size, self.snake_size])

            # Draw the food
            pygame.draw.rect(screen, (255, 0, 0), [self.env.food_c * self.snake_size, self.env.food_r * self.snake_size, self.snake_size, self.snake_size])

            pygame.display.update()  # Update the display
            pygame.time.delay(100)  # Delay to control the speed of the game

            if self.env.game_close:
                print(f"Game Over! Snake Length: {self.env.snake_length}")
                self.game_over = True

def main():
    # Training Phase
    episodes = 5000  # Number of training episodes
    agent = SnakeQAgent(episodes)
    agent.train()  # Start training the agent

    # Load the trained Q-table for testing
    with open('Q_table_results/5000.pickle', 'rb') as file:
        q_table = pickle.load(file)

    # Testing Phase
    visualizer = SnakeGameVisualizer(q_table)
    visualizer.draw_elements()  # Start the visualization of the trained agent

if __name__ == "__main__":
    main()
