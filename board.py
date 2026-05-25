OPERATOR_MAP = {
    (0,1):'+', (0,3):'-', (0,5):'x', (0,7):'/',
    (1,0):'/', (1,2):'x', (1,4):'-', (1,6):'+',
    (2,1):'+', (2,3):'-', (2,5):'x', (2,7):'/',
    (3,0):'/', (3,2):'x', (3,4):'-', (3,6):'+',
    (4,1):'+', (4,3):'-', (4,5):'x', (4,7):'/',
    (5,0):'/', (5,2):'x', (5,4):'-', (5,6):'+',
    (6,1):'+', (6,3):'-', (6,5):'x', (6,7):'/',
    (7,0):'/', (7,2):'x', (7,4):'-', (7,6):'+'
}

class Piece:
    def __init__(self, player, value, is_dama=False):
        self.player  = player
        self.value   = value
        self.is_dama = is_dama

def initialize_board():
    board  = [[None]*8 for _ in range(8)]
    p0_v   = [0,1,2,3,4,5,6,7]
    p0_pos = [(6,1),(6,3),(6,5),(6,7),(7,0),(7,2),(7,4),(7,6)]
    p1_v   = [8,9,10,11,12,13,14,15]
    p1_pos = [(0,1),(0,3),(0,5),(0,7),(1,0),(1,2),(1,4),(1,6)]
    for i,p in enumerate(p0_pos):
        board[p[0]][p[1]] = Piece(0, p0_v[i])
    for i,p in enumerate(p1_pos):
        board[p[0]][p[1]] = Piece(1, p1_v[i])
    return board