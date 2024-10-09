# LearnSnake.py

import random
import numpy as np
import pickle

class LearnSnake:
    def __init__(self):         
        self.screen_width = 600
        self.screen_height = 400
        self.snake_size = 10
        self.snake_speed = 10
        self.snake_coords = []
        self.snake_length = 1
        self.dir = "right"
        self.board = np.zeros((self.screen_height // self.snake_size, self.screen_width // self.snake_size))
        self.game_close = False
        self.x1 = self.screen_width / 2
        self.y1 = self.screen_height / 2
        self.r1, self.c1 = self.coords_to_index(self.x1, self.y1)
        self.board[self.r1][self.c1] = 1
        self.c_change = 1
        self.r_change = 0
        self.food_r, self.food_c = self.generate_food()
        self.board[self.food_r][self.food_c] = 2
        self.survived = 0
        self.step()
    
    def get_state(self):
        head_r, head_c = self.snake_coords[-1]
        state = [
            int(self.dir == "left"),
            int(self.dir == "right"),
            int(self.dir == "up"),
            int(self.dir == "down"),
            int(self.food_r < head_r),
            int(self.food_r > head_r),
            int(self.food_c < head_c),
            int(self.food_c > head_c),
            self.is_unsafe(head_r + 1, head_c),
            self.is_unsafe(head_r - 1, head_c),
            self.is_unsafe(head_r, head_c + 1),
            self.is_unsafe(head_r, head_c - 1)
        ]
        return tuple(state)
    
    def is_unsafe(self, r, c):
        if self.valid_index(r, c):
            return 1 if self.board[r][c] == 1 else 0
        return 1

    def valid_index(self, r, c):
        return 0 <= r < len(self.board) and 0 <= c < len(self.board[0])

    def coords_to_index(self, x, y):
        r = int(y // self.snake_size)
        c = int(x // self.snake_size)
        return (r, c)

    def generate_food(self):
        food_c = int(round(random.randrange(0, self.screen_width - self.snake_size) / 10.0))
        food_r = int(round(random.randrange(0, self.screen_height - self.snake_size) / 10.0))
        if self.board[food_r][food_c] != 0:
            return self.generate_food()
        return food_r, food_c

    def game_over(self):
        return self.game_close

    def step(self, action="None"):
        if action == "None":
            action = random.choice(["left", "right", "up", "down"])
        else:
            action = ["left", "right", "up", "down"][action]

        reward = 0
        if action == "left" and (self.dir != "right" or self.snake_length == 1):
            self.c_change = -1
            self.r_change = 0
            self.dir = "left"
        elif action == "right" and (self.dir != "left" or self.snake_length == 1):
            self.c_change = 1
            self.r_change = 0
            self.dir = "right"
        elif action == "up" and (self.dir != "down" or self.snake_length == 1):
            self.r_change = -1
            self.c_change = 0
            self.dir = "up"
        elif action == "down" and (self.dir != "up" or self.snake_length == 1):
            self.r_change = 1
            self.c_change = 0
            self.dir = "down"

        # Check boundaries
        if self.c1 >= self.screen_width // self.snake_size or self.c1 < 0 or self.r1 >= self.screen_height // self.snake_size or self.r1 < 0:
            self.game_close = True

        self.c1 += self.c_change
        self.r1 += self.r_change
        self.snake_coords.append((self.r1, self.c1))

        if self.valid_index(self.r1, self.c1):
            self.board[self.r1][self.c1] = 1
        
        if len(self.snake_coords) > self.snake_length:
            rd, cd = self.snake_coords[0]
            del self.snake_coords[0]
            if self.valid_index(rd, cd):
                self.board[rd][cd] = 0
        
        for r, c in self.snake_coords[:-1]:
            if r == self.r1 and c == self.c1:
                self.game_close = True
        
        if self.c1 == self.food_c and self.r1 == self.food_r:
            self.food_r, self.food_c = self.generate_food()
            self.board[self.food_r][self.food_c] = 2
            self.snake_length += 1
            reward = 1  # Food eaten

        if self.game_close:
            reward = -10  # Game over

        self.survived += 1    
        return self.get_state(), reward, self.game_close

    def run_game(self, episode):
        filename = f"Q_table_results/{episode}.pickle"
        with open(filename, 'rb') as file:
            table = pickle.load(file)

        current_length = 2
        steps_unchanged = 0
        while not self.game_over():
            state = self.get_state()
            action = np.argmax(table[state])
            if steps_unchanged == 1000:
                break
            self.step(action)
            if self.snake_length != current_length:
                steps_unchanged = 0
                current_length = self.snake_length
            else:
                steps_unchanged += 1
        
        return self.snake_length
