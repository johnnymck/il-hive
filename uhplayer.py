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