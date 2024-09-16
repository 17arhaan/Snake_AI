import random
import numpy as np
import pygame
import pickle
import time
class Color:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.neon_red = (255, 0, 0)
        self.cyan = (0, 255, 255)
        self.blue = (0, 0, 255)
class SnakeGame:
    def __init__(self):
        self.show_episode = True
        self.episode = None
        self.scale = 2
        self.w = int(600 * self.scale)
        self.h = int(400 * self.scale)
        self.pad = int(30 * self.scale)
        self.sn_size = int(10 * self.scale)
        self.fd_size = int(10 * self.scale)
        self.spd = 20
        self.sn_coords = []
        self.sn_len = 1
        self.dir = "right"
        self.board = np.zeros((self.h // self.sn_size, self.w // self.sn_size))
        self.game_close = False
        self.x = self.w / 2
        self.y = self.h / 2 + self.pad
        self.r, self.c = self.coord_to_idx(self.x, self.y)
        self.board[self.r][self.c] = 1
        self.col_chg = 1
        self.row_chg = 0
        self.fd_r, self.fd_c = self.mk_food()
        self.board[self.fd_r][self.fd_c] = 2
        self.surv = 0
        pygame.init()
        self.color = Color()
        self.screen = pygame.display.set_mode((self.w, self.h + self.pad))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("bahnschrift", int(18 * self.scale))
        self.last_dir = None
        self.step()
    def show_score(self, score):
        text = self.font.render(f"Score: {score}", True, self.color.white)
        self.screen.blit(text, [500 * self.scale, 10])
    def draw_snake(self):
        for i in range(len(self.sn_coords) - 1, -1, -1):
            row, col = self.sn_coords[i]
            x, y = self.idx_to_coord(row, col)
            if i == len(self.sn_coords) - 1:
                pygame.draw.rect(self.screen, self.color.blue, [x, y, self.sn_size, self.sn_size])  # Head
            else:
                pygame.draw.rect(self.screen, self.color.cyan, [x, y, self.sn_size, self.sn_size])  # Body
    def game_end_msg(self):
        msg = self.font.render("Game over!", True, self.color.neon_red)
        self.screen.blit(msg, [2 * self.w / 5, 2 * self.h / 5 + self.pad])
    def is_unsafe(self, row, col):
        if self.valid_idx(row, col):
            if self.board[row][col] == 1:
                return 1
            return 0
        else:
            return 1
    def get_state(self):
        hr, hc = self.sn_coords[-1]
        state = []
        state.append(int(self.dir == "left"))
        state.append(int(self.dir == "right"))
        state.append(int(self.dir == "up"))
        state.append(int(self.dir == "down"))
        state.append(int(self.fd_r < hr))
        state.append(int(self.fd_r > hr))
        state.append(int(self.fd_c < hc))
        state.append(int(self.fd_c > hc))
        state.append(self.is_unsafe(hr + 1, hc))
        state.append(self.is_unsafe(hr - 1, hc))
        state.append(self.is_unsafe(hr, hc + 1))
        state.append(self.is_unsafe(hr, hc - 1))
        return tuple(state)
    def valid_idx(self, row, col):
        return 0 <= row < len(self.board) and 0 <= col < len(self.board[0])
    def idx_to_coord(self, row, col):
        x = col * self.sn_size
        y = row * self.sn_size + self.pad
        return (x, y)
    def coord_to_idx(self, x, y):
        row = int((y - self.pad) // self.sn_size)
        col = int(x // self.sn_size)
        return (row, col)
    def mk_food(self):
        col = int(round(random.randrange(0, self.w - self.fd_size) / self.fd_size))
        row = int(round(random.randrange(0, self.h - self.fd_size) / self.fd_size))
        if self.board[row][col] != 0:
            row, col = self.mk_food()
        return row, col
    def game_over(self):
        return self.game_close
    def step(self, action="None"):
        if action == "None":
            action = random.choice(["left", "right", "up", "down"])
        else:
            action = ["left", "right", "up", "down"][action]
        for event in pygame.event.get():
            pass
        self.last_dir = self.dir
        if action == "left" and (self.dir != "right" or self.sn_len == 1):
            self.col_chg = -1
            self.row_chg = 0
            self.dir = "left"
        elif action == "right" and (self.dir != "left" or self.sn_len == 1):
            self.col_chg = 1
            self.row_chg = 0
            self.dir = "right"
        elif action == "up" and (self.dir != "down" or self.sn_len == 1):
            self.row_chg = -1
            self.col_chg = 0
            self.dir = "up"
        elif action == "down" and (self.dir != "up" or self.sn_len == 1):
            self.row_chg = 1
            self.col_chg = 0
            self.dir = "down"
        if self.c >= self.w // self.sn_size or self.c < 0 or self.r >= self.h // self.sn_size or self.r < 0:
            self.game_close = True
        self.c += self.col_chg
        self.r += self.row_chg
        self.screen.fill(self.color.black)
        pygame.draw.rect(self.screen, self.color.white, (0, self.pad, self.w, self.h), 1)
        fd_x, fd_y = self.idx_to_coord(self.fd_r, self.fd_c)
        pygame.draw.rect(self.screen, self.color.neon_red, [fd_x, fd_y, self.fd_size, self.fd_size])
        self.sn_coords.append((self.r, self.c))
        if self.valid_idx(self.r, self.c):
            self.board[self.r][self.c] = 1
        if len(self.sn_coords) > self.sn_len:
            r_del, c_del = self.sn_coords[0]
            del self.sn_coords[0]
            if self.valid_idx(r_del, c_del):
                self.board[r_del][c_del] = 0
        for r, c in self.sn_coords[:-1]:
            if r == self.r and c == self.c:
                self.game_close = True
        self.draw_snake()
        self.show_score(self.sn_len - 1)
        pygame.display.update()
        if self.c == self.fd_c and self.r == self.fd_r:
            self.fd_r, self.fd_c = self.mk_food()
            self.board[self.fd_r][self.fd_c] = 2
            self.sn_len += 1
        self.surv += 1
    def run(self, ep):
        self.show_episode = True
        self.episode = ep
        pygame.display.update()
        fname = f"Q_table_results/{ep}.pickle"
        with open(fname, 'rb') as file:
            table = pickle.load(file)
        time.sleep(5)
        cur_len = 2
        unchanged_steps = 0
        while not self.game_over():
            if self.sn_len != cur_len:
                unchanged_steps = 0
                cur_len = self.sn_len
            else:
                unchanged_steps += 1
            state = self.get_state()
            action = np.argmax(table[state])
            if unchanged_steps == 1000:
                break
            self.step(action)
            self.clock.tick(self.spd)
        if self.game_over():
            self.screen.fill(self.color.black)
            pygame.draw.rect(self.screen, self.color.white, (0, self.pad, self.w, self.h), 1)
            self.game_end_msg()
            self.show_score(self.sn_len - 1)
            pygame.display.update()
            time.sleep(2)
        pygame.quit()
if __name__ == "__main__":
    game = SnakeGame()
    try :
        game.run(100000)
    except KeyboardInterrupt:
        print("\t\t\t\t\t\t\t!!!Done Already!!!")