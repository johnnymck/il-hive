"""A python AI for Hive, by John Yianni
"""

__author__ = "William Dizon"
__license__ = "Simplified BSD License"
__version__ = "0.0.1"
__email__ = "wdchromium@gmail.com"

from enum import Enum
from collections import namedtuple

Tile = namedtuple('Tile', ['color', 'insect'])
Log = namedtuple('Ply', ['piece', 'origin', 'dest'])

class Insect(Enum):
    Queen = 0
    Ant = 1
    Beetle = 2
    Grasshopper = 3
    Spider = 4
    Mosquito = 5
    Ladybug = 6
    Pillbug = 7
    
class Color(Enum):
    White = 0
    Black = 1
    
class Pointed_Directions(Enum):
    NE = (1,-1)
    E = (1,0)
    SE = (0,1)
    SW = (-1,1)
    W = (-1,0)
    NW = (0,-1)
    
class Flat_Directions(Enum):
    N = (0,1)
    NE = (1,1)
    SE = (1,0)
    S = (0,-1)
    SW = (-1,-1)
    NW = (-1,0)

class HiveBoard(object):
    def __init__(self, tile_orientation = Flat_Directions):
        self._pieces = {}
        self._log = []
        self.tile_orientation = tile_orientation
        
    def __len__(self):
        return 0
        
    def __getitem__(self, key):
        return self._pieces[key]
        
    def place(self, tile, coords):
        if coords in self._pieces:
            raise RuntimeError
        self._pieces[coords] = [tile]
        self._log.append(Log(tile, coords, None))
    
    def pop(self, coords):
        p = self._pieces[coords].pop()
        if not self._pieces[coords]:
            del self._pieces[coords]
        return p
        
    def piece_at(self, coords):
        return self._pieces[coords][-1]
        
    def stack_at(self, coords):
        return self._pieces[coords]
        
    def move(self, origin, dest):
        p = self.pop(origin)
        if dest in self._pieces:
            self._pieces[dest].append(p)
        else:
            self._pieces[dest] = [p]
        self._log.append(Log(p, origin, dest))
    
    def act(self, acting_piece_coords, origin, dest):
        def queen_placed(color):
            for stack in self._pieces.values():
                if Tile(color, Insect.Queen) in stack:
                    return True
            return False
            
        acting_piece = self.piece_at(acting_piece_coords)

        if origin and dest and \
            not queen_placed(acting_piece.color):
            raise IllegalMovement(acting_piece, origin, dest)
    
    @staticmethod
    def hex_neighbors(tile_orientation, origin):
        return set([tuple(sum(x) for x in zip(origin, d.value))
                    for d in tile_orientation])

class IllegalMovement(Exception):
    def __init__(self, actor, origin, dest):
        self.actor = actor
        self.origin = origin
        self.dest = dest
        
        self.message = 'Cannot move any pieces until Queen has been placed'

class IllegalPlacement(Exception):
    def __init__(self, actor, dest):
        self.actor = actor
        self.dest = dest
        
        self.message = 'Cannot place {0} at {1}'.format(actor, dest)