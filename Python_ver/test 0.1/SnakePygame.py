import pygame
import os
import numpy as np
from LearnSnake import LearnSnake
from Snake_QLearning import SnakeQAgent
import time  # Import time for timing key presses

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        self.font = pygame.font.SysFont('Arial', 30)

        # Initialize game variables
        self.agent = None
        self.leaderboard = []
        self.last_esc_press_time = 0  # Track the last time Esc was pressed
        self.esc_press_interval = 0.5  # Time interval to consider double Esc press (in seconds)

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.fullscreen = not self.fullscreen

    def show_menu(self):
        while True:
            self.screen.fill((0, 0, 0))
            title = self.font.render("Snake Game - Q-Learning", True, (255, 255, 255))
            start_text = self.font.render("Press ENTER to Start", True, (255, 255, 255))
            toggle_text = self.font.render("Press F to Toggle Fullscreen", True, (255, 255, 255))
            leaderboard_text = self.font.render("Press L for Leaderboard", True, (255, 255, 255))
            quit_text = self.font.render("Press Q to Quit", True, (255, 255, 255))

            self.screen.blit(title, (self.screen_width // 4, self.screen_height // 4))
            self.screen.blit(start_text, (self.screen_width // 4, self.screen_height // 4 + 40))
            self.screen.blit(toggle_text, (self.screen_width // 4, self.screen_height // 4 + 80))
            self.screen.blit(leaderboard_text, (self.screen_width // 4, self.screen_height // 4 + 120))
            self.screen.blit(quit_text, (self.screen_width // 4, self.screen_height // 4 + 160))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.run_game()  # Start the game
                    elif event.key == pygame.K_f:
                        self.toggle_fullscreen()  # Toggle fullscreen
                    elif event.key == pygame.K_l:
                        self.show_leaderboard()  # Show leaderboard
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_ESCAPE:
                        self.handle_double_esc()  # Handle double Esc press

    def handle_double_esc(self):
        current_time = time.time()
        if current_time - self.last_esc_press_time <= self.esc_press_interval:
            pygame.quit()  # Quit the game if double Esc is pressed
            quit()
        else:
            self.last_esc_press_time = current_time  # Update last Esc press time

    def show_leaderboard(self):
        while True:
            self.screen.fill((0, 0, 0))
            title = self.font.render("Leaderboard", True, (255, 255, 255))
            self.screen.blit(title, (self.screen_width // 4, self.screen_height // 4))

            # Display leaderboard
            for i, score in enumerate(sorted(self.leaderboard, reverse=True)[:10]):
                score_text = self.font.render(f"{i + 1}. {score}", True, (255, 255, 255))
                self.screen.blit(score_text, (self.screen_width // 4, self.screen_height // 4 + 40 + i * 30))

            back_text = self.font.render("Press B to go back", True, (255, 255, 255))
            self.screen.blit(back_text, (self.screen_width // 4, self.screen_height // 4 + 300))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        return  # Go back to menu

    def run_game(self):
        self.agent = SnakeQAgent(episodes=1000)
        self.agent.train()

        # Main game loop
        while self.running:
            self.screen.fill((0, 0, 0))
            state, reward, done = self.agent.env.step(action=self.agent.choose_action(self.agent.env.get_state()))
            score = self.agent.env.snake_length - 1
            
            # Draw the snake
            for segment in self.agent.env.snake_coords:
                pygame.draw.rect(self.screen, (0, 255, 0), (segment[1] * self.agent.env.snake_size,
                                                            segment[0] * self.agent.env.snake_size,
                                                            self.agent.env.snake_size,
                                                            self.agent.env.snake_size))
            # Draw the food
            pygame.draw.rect(self.screen, (255, 0, 0), (self.agent.env.food_c * self.agent.env.snake_size,
                                                          self.agent.env.food_r * self.agent.env.snake_size,
                                                          self.agent.env.snake_size,
                                                          self.agent.env.snake_size))

            # Display score
            score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(10)  # Control the game speed

            if done:
                self.leaderboard.append(score)
                self.agent.env = LearnSnake()  # Reset the environment

    def main(self):
        self.show_menu()

if __name__ == "__main__":
    game = SnakeGame()
    game.main()
