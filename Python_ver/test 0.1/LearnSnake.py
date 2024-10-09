import random
import numpy as np
import pickle

class LearnSnake:
    def __init__(self):         
        self.screen_width = 800
        self.screen_height = 600
        self.snake_size = 20
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
        state = []
        state.append(int(self.dir == "left"))
        state.append(int(self.dir == "right"))
        state.append(int(self.dir == "up"))
        state.append(int(self.dir == "down"))
        state.append(int(self.food_r < head_r))
        state.append(int(self.food_r > head_r))
        state.append(int(self.food_c < head_c))
        state.append(int(self.food_c > head_c))
        state.append(self.is_unsafe(head_r + 1, head_c))
        state.append(self.is_unsafe(head_r - 1, head_c))
        state.append(self.is_unsafe(head_r, head_c + 1))
        state.append(self.is_unsafe(head_r, head_c - 1))
        return tuple(state)

    def is_unsafe(self, r, c):
        return 1 if not self.valid_index(r, c) or self.board[r][c] == 1 else 0

    def valid_index(self, r, c):
        return 0 <= r < len(self.board) and 0 <= c < len(self.board[0])

    def coords_to_index(self, x, y):
        r = int(y // self.snake_size)
        c = int(x // self.snake_size)
        return (r, c)

    def generate_food(self):
        while True:
            food_c = int(round(random.randrange(0, self.screen_width - self.snake_size) / self.snake_size))
            food_r = int(round(random.randrange(0, self.screen_height - self.snake_size) / self.snake_size))
            if self.board[food_r][food_c] == 0:
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

        self.c1 += self.c_change
        self.r1 += self.r_change
        self.snake_coords.append((self.r1, self.c1))

        if self.valid_index(self.r1, self.c1):
            self.board[self.r1][self.c1] = 1
        else:
            self.game_close = True

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
            reward = 1  # Food reward
        else:
            reward = 0

        if self.game_close:
            reward = -10  # Dead

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
            self.step(action)
            if self.snake_length != current_length:
                steps_unchanged = 0
                current_length = self.snake_length
            else:
                steps_unchanged += 1
            if steps_unchanged == 1000:
                break
        return self.snake_length
