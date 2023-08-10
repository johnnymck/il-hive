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
        self.centre_offset = (13, 13)
        self.color = hive.Color.White

        self.placement_action_space = spaces.Discrete(self.num_piece_types * self.grid_size * self.grid_size)
        self.movement_action_space = spaces.MultiDiscrete([
            self.num_piece_types,  # Piece type
            self.grid_size,        # From row
            self.grid_size,        # From column
            self.grid_size,        # To row
            self.grid_size         # To column
        ])
        self.observation_space = spaces.Box(low=0, high=self.num_piece_types, shape=(self.grid_size, self.grid_size, 2), dtype=np.int32)
        self.board = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        self.current_player = 1
        self.num_moves = 0

    def reset(self, seed=None):
        super().reset(seed=seed)#this line was annoying btw!
        # Reset the environment and return the initial observation
        self.board = np.zeros((self.grid_size, self.grid_size), dtype=np.int32)
        self.current_player = 1
        self.num_moves = 0
        self.hive = hive.HiveBoard(queen_opening_allowed=True)
        return (self.board.copy(), spaces.Discrete(len(self._get_all_actions(self.color))))
    
    def step(self, action):
        if action < self.placement_action_space.n:  # Placement action
            piece_type = action // (self.grid_size * self.grid_size)
            row = (action % (self.grid_size * self.grid_size)) // self.grid_size
            col = (action % (self.grid_size * self.grid_size)) % self.grid_size
            
            # Perform placement logic here
            # ...
            
        else:  # Movement action
            piece_type, from_row, from_col, to_row, to_col = self.movement_action_space[action - self.placement_action_space.n]
            
            # Perform movement logic here
            # ...
        
        # Update the environment state, calculate reward, done, and info
        
        return self.board.copy(), reward, done, info
    
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