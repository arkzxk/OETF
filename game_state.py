import copy
from board import initialize_board, OPERATOR_MAP

def compute_score(att, dfn, op, is_dama):
    if   op == '+': res = att + dfn
    elif op == '-': res = att - dfn
    elif op == 'x': res = att * dfn
    elif op == '/': res = att / dfn if dfn != 0 else 0
    else:           res = 0
    return res * 2 if is_dama else res

def simulate(state, move):
    s = copy.deepcopy(state)
    s.apply_move(move)
    return s

class GameState:
    def __init__(self):
        self.board  = initialize_board()
        self.scores = {0: 0, 1: 0}
        self.active = 0
        self.turn   = 0

    def apply_move(self, move):
        pc = self.board[move[0][0]][move[0][1]]
        captured_squares = []

        for i in range(1, len(move)):
            r,  c  = move[i]
            mr, mc = (move[i-1][0] + r) // 2, (move[i-1][1] + c) // 2

            cap = self.board[mr][mc]
            if cap and (mr, mc) not in captured_squares:
                op = OPERATOR_MAP.get((mr, mc), '+')
                sc = compute_score(pc.value, cap.value, op, pc.is_dama)
                self.scores[self.active] += sc
                self.board[mr][mc] = None
                captured_squares.append((mr, mc))

        self.board[move[0][0]][move[0][1]] = None
        self.board[r][c] = pc

        if (self.active == 0 and r == 0) or \
           (self.active == 1 and r == 7):
            pc.is_dama = True

        self.active = 1 - self.active
        self.turn  += 1