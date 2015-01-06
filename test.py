import unittest
import hive

class TestHive(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_board(self):
        board = hive.HiveBoard()
        self.assertEqual(len(board), 0)
        self.assertIs(board.tile_orientation, hive.Flat_Directions)
        
        board = hive.HiveBoard(hive.Flat_Directions)
        self.assertIs(board.tile_orientation, hive.Flat_Directions)
        
        board = hive.HiveBoard(hive.Pointed_Directions)
        self.assertIs(board.tile_orientation, hive.Pointed_Directions)
    
    def test_tiles(self):
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        self.assertEqual(piece.color, hive.Color.White)
        self.assertEqual(piece.insect, hive.Insect.Queen)
        
    def test_place(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0))
        self.assertEqual(board.piece_at((0,0)).color, hive.Color.White)
        self.assertEqual(board.piece_at((0,0)).insect, hive.Insect.Queen)
        
        piece_2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)
        with self.assertRaises(RuntimeError):
            board.place(piece_2, (0,0))
            
    def test_pop(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        with self.assertRaises(KeyError):
            board.pop((0,0))
        
        board.place(piece, (0,0))
        p = board.pop((0,0))
        
        self.assertIs(piece, p)
        
        with self.assertRaises(KeyError):
            board.piece_at((0,0))

        with self.assertRaises(KeyError):
            board.pop((0,0))

    def test_piece_at(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0))
        self.assertEqual(board.piece_at((0,0)).color, hive.Color.White)
        self.assertEqual(board.piece_at((0,0)).insect, hive.Insect.Queen)
    
    def test_stack_at(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        piece_2 = hive.Tile(hive.Color.Black, hive.Insect.Ant)

        board.place(piece, (0,0))
        with self.assertRaises(RuntimeError):
            board.place(piece_2, (0,0))
            
    def test_move(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0))
        board.move((0,0), (0,1))
        
        with self.assertRaises(KeyError):
            board.piece_at((0,0))
            
        self.assertEqual(board.piece_at((0,1)).color, hive.Color.White)
        self.assertEqual(board.piece_at((0,1)).insect, hive.Insect.Queen)
    
    def test_log(self):
        board = hive.HiveBoard()
        piece = hive.Tile(hive.Color.White, hive.Insect.Queen)
        
        board.place(piece, (0,0))
        board.move((0,0), (0,1))
        
        self.assertIs(board._log[0].piece, piece)
        self.assertEqual(board._log[0].origin, (0,0))
        self.assertEqual(board._log[0].dest, None)
        
        self.assertIs(board._log[1].piece, piece)
        self.assertEqual(board._log[1].origin, (0,0))
        self.assertEqual(board._log[1].dest, (0,1))
        
        with self.assertRaises(KeyError):
            board.move((0,0), (0,1))
        
        board.move((0,1), (1,1))
        self.assertIs(board._log[2].piece, piece)
        self.assertEqual(board._log[2].origin, (0,1))
        self.assertEqual(board._log[2].dest, (1,1))
        
    def test_hex_neighbors(self):
        board = hive.HiveBoard(hive.Flat_Directions)
        self.assertSetEqual(board.hex_neighbors(board.tile_orientation, (0,0)),
                            set([(0,1), (1,1), (1,0), 
                                 (0,-1), (-1,-1), (-1,0)]))
                                 
    def test_prequeen_movement_rule(self):
        board = hive.HiveBoard()

        board.place(hive.Tile(hive.Color.White, hive.Insect.Ant), (0,0))
        board.place(hive.Tile(hive.Color.Black, hive.Insect.Ant), (0,1))
        
        with self.assertRaises(hive.IllegalMovement):
            board.act((0,0), (0,0), (0,1))
        
        with self.assertRaises(hive.IllegalMovement):
            board.act((0,0), (0,0), (1,0))
        
        board.place(hive.Tile(hive.Color.White, hive.Insect.Queen), (0,-1))
        board.place(hive.Tile(hive.Color.White, hive.Insect.Beetle), (1,-1))
        board.act((1,-1), (1,-1), (1,0))
        

if __name__ == '__main__':
    unittest.main()