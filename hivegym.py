import gymnasium as gym
import numpy as np
import hive

from gymnasium import spaces
from stable_baselines3.common.env_checker import check_env

class HiveEnv(gym.Env):
    """Hive game Environment that implements StableBaselines3's gym interface."""
    def __init__(self):
        super().__init__()
        self.grid_size = 28
        self.num_piece_types = 8 # ant, grasshopper, beetle, spider, queen, pillbug, mosquito, ladybug
        self.max_moves = 149 # end it before we get to 150 moves because that would be mental
        self.hive = hive.HiveBoard(queen_opening_allowed=True)
        self.centre_offset = 13
        self.color = hive.Color.White
        self.observation_space = spaces.Box(low=0, high=self.num_piece_types, shape=(self.grid_size, self.grid_size), dtype=np.int8)
        self.board = np.zeros((self.grid_size, self.grid_size), dtype=np.int8)
        self.current_player = 1
        self.num_moves = 0

    def reset(self, seed=None):
        super().reset(seed=seed)#this line was annoying btw!
        # Reset the environment and return the initial observation
        self.color = hive.Color.White
        self.board = np.zeros((self.grid_size, self.grid_size), dtype=np.int8)
        self.current_player = 1
        self.num_moves = 0
        self.hive = hive.HiveBoard(queen_opening_allowed=True)
        return (self.board.copy(), spaces.Discrete(len(self._get_all_actions())))
    
    def step(self, action):
        self.num_moves += 1
        actions = self._get_all_actions()
        print(actions[action])
        piece, from_x, from_y, to_x, to_y = actions[action]
        term = False
        trunc = False
        if from_x == -1 and from_y == -1:
            piece_obj = self._get_tile_from_encoding(piece)
            self.hive.place(piece_obj, (to_x, to_y))
        else:
            self.hive.move((from_x , from_y), (to_x, to_y))
        if self.hive.winner == self.color:
            reward = 1
            term = True
        elif self.hive.winner == False:
            # draw
            reward = 0
            term = True
        elif self.hive.winner == None:
            # no winnder, no reward, game continues
            reward = 0
        else:
            # lost - negative reward, game over
            reward = -1
            term = True
        if self.num_moves > self.max_moves:
            trunc = True
        if self.color == hive.Color.White:
            self.color = hive.Color.Black
        else:
            self.color = hive.Color.White
        self._push_hive_to_grid()
        #expects (obs_state, reward, terminal, truncated, info)
        return (self.board.copy(), reward, term, trunc, {})

    def _push_hive_to_grid(self):
        for coords, stack in self.hive.get_pieces():
            self.board[coords[0]+self.centre_offset][coords[1]+self.centre_offset] = self._get_tile_encoding(stack[-1])
    
    def _get_tile_encoding(self, tile):
        """Quick and dirty method to translate pieces into a simple integer to hopefully
        represent state enough for the IL to understand"""
        total = 0
        if tile.color == hive.Color.Black:
            total += 100
        if tile.insect == hive.Insect.Ant:
            total += 10
        elif tile.insect == hive.Insect.Beetle:
            total += 20
        elif tile.insect == hive.Insect.Grasshopper:
            total += 30
        elif tile.insect == hive.Insect.Spider:
            total += 40
        elif tile.insect == hive.Insect.Queen:
            total += 50
        elif tile.insect == hive.Insect.Ladybug:
            total += 60
        elif tile.insect == hive.Insect.Pillbug:
            total += 70
        elif tile.insect == hive.Insect.Mosquito:
            total += 80
        if tile.number == 1:
            total += 1
        elif tile.number == 2:
            total += 2
        elif tile.number == 3:
            total += 3
        return total

    def _get_tile_from_encoding(self, encoding):
        encoding = str(encoding)
        output_string = ''
        if len(encoding) == 3:
            output_string += 'b'
        else:
            output_string += 'w'
        if encoding[-2] == '1':
            output_string += 'A'
        elif encoding[-2] == '2':
            output_string += 'B'
        elif encoding[-2] == '3':
            output_string += 'G'
        elif encoding[-2] == '4':
            output_string += 'S'
        elif encoding[-2] == '5':
            output_string += 'Q'
        elif encoding[-2] == '6':
            output_string += 'L'
        elif encoding[-2] == '7':
            output_string += 'P'
        elif encoding[-2] == '8':
            output_string += 'M'
        if encoding[-1] == '1':
            output_string += '1'
        elif encoding[-1] == '2':
            output_string += '2'
        elif encoding[-1] == '3':
            output_string += '3'
        return hive.Tile.from_string(output_string)
    
    def _action_with_grid_offset(self, piece, move):
        from_x = move[0][0] + self.centre_offset[0]
        from_y = move[0][1] + self.centre_offset[1]
        to_x = move[1][0] + self.centre_offset[0]
        to_y = move[1][1] + self.centre_offset[1]
        return (piece, from_x, from_y, to_x, to_y)
    
    def _get_all_actions(self):
        actions = []
        for move in self.hive.all_moves_as_tuples(self.color):
            piece = self._get_tile_encoding(self.hive.piece_at(move[0]))
            actions.apend(self._action_with_grid_offset(piece, move))
        
        for placement in self.hive.valid_placements(self.color):
            for piece in self.hive.available_pieces_from_hand(self.color):
                actions.append((self._get_tile_encoding(piece), -1, -1, placement[0], placement[1]))
        
        return actions

    @property
    def action_space(self):
        return spaces.Discrete(len(self._get_all_actions()))

if __name__ == '__main__':
    hivegym = HiveEnv()
    check_env(hivegym)