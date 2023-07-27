#!/usr/bin/env python

import agents
import uhplayer
import hive

if __name__ == '__main__':
    board = hive.HiveBoard()
    agent = agents.RandomMoveAgent(board, hive.Color.White)
    mzinga_com = uhplayer.UhpLayer(agent)
    print('ok')
    while True:
        mzinga_com.repl()
