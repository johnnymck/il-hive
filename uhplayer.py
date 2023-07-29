"""UhpLayer.py
Glue library for interfacing agents with Mzinga Viewer https://github.com/jonthysell/Mzinga using Universal Hive Protocol (UHP)
"""

import hive

class UhpLayer(object):
    def __init__(self, agent, ident_string):
        self.agent = agent
        self.ident_string = ident_string
        # print engine metadata
        print('id ' + self.ident_string)
        print('Mosquito;Ladybug;Pillbug')
        print('ok')    
    def repl(self):
        #read
        x = input()
        #eval
        output = None
        if x == 'GameTypeString':
            output = self.game_string()
        elif x == 'GameStateString':
            output = self.game_state_string()
        elif x == 'info':
            output = 'id ' + self.ident_string
        #print
        print(output)
        print('ok')

    def game_state_string(self):
        if self.agent.board.winner == None:
            return 'InProgress'
        elif self.agent.board.winner == False:
            return 'Draw'
        else:
            if self.agent.board.winner() == hive.Color.Black:
                return 'BlackWins'
            elif self.agent.board.winner() == hive.Color.White:
                return 'WhiteWins'
            else:
                raise Exception()
    
    def game_string(self):
        return 'Base+MLP'

    def gen_valid_moves(self):
        in_play = self.agent.board.pieces_in_play
        if not in_play:
            if self.agent.color == hive.Color.White:
                return 'wA1;wB1;wS1;wG1;wP;wM;wL'
            else:
                return 'bA1;bB1;bS1;bG1;bP;bM;bL'
        else:
            moves = [str(i) for i in self.agent.board.free_pieces(self.agent.color)]
            return ';'.join(moves)
    
    def best_move(self):
        return 