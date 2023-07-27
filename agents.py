"""AGENTS.py
Library contaning agents
"""

import hive

from random import choice, randint

class RandomMoveAgent(object):
    def __init__(self, board, color):
        self.board = board
        self.color = color
        if color == hive.Color.Black:
            self.my_pieces = [hive.Tile.from_string(i) for i in ('bA1', 'bA2', 'bA3', 'bG1', 'bG2', 'bG3', 'bS1', 'bS2', 'bB1', 'bB2', 'bL', 'bP', 'bM', 'bQ')]
        else:
            self.my_pieces = [hive.Tile.from_string(i) for i in ('wA1', 'wA2', 'wA3', 'wG1', 'wG2', 'wG3', 'wS1', 'wS2', 'wB1', 'wB2', 'wL', 'wP', 'wM', 'wQ')]

    def pick_random_move(self):
        moves_on_board = list(self.board.all_moves_as_tuples(self.color))
        return choice(moves_on_board)
    
    def place_random_piece(self):
        placement = choice(list(self.board.valid_placements(self.color)))
        piece = choice(self.unplayed_pieces)
        return piece, placement

    def move(self):
        """ Pick EITHER random move OR random placement, placements more likely at the beginning """
        factor = len(self.my_pieces) - len(self.unplayed_pieces)
        thing = randint(0, 14)
        if factor < thing:
            return self.place_random_piece()
        else:
            return self.pick_random_move()
    
    @property
    def unplayed_pieces(self):
        return [i for i in self.my_pieces if i not in self.board.pieces_in_play]