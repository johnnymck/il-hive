#!/usr/bin/env python

import agents
import uhplayer
import hive

if __name__ == '__main__':
    board = hive.HiveBoard()
    agent = agents.RandomMoveAgent(board, hive.Color.White)
    mzinga_com = uhplayer.UhpLayer(agent, 'RandomAgent v0.0.1 (author: johnny mckenzie)')
    print(mzinga_com.ident_string)
    print('ok')
    while True:
        mzinga_com.repl()
