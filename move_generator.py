def get_legal_moves(state):
    caps = get_captures(state)
    return caps if caps else get_walks(state)

def get_captures(state):
    result,p = [],state.active
    for r in range(8):
        for c in range(8):
            pc = state.board[r][c]
            if pc and pc.player==p:
                find_caps(state,r,c,[(r,c)],result)
    return result

def find_caps(state,r,c,path,result):
    pc    = state.board[path[0][0]][path[0][1]]
    dirs  = [(-1,-1),(-1,1),(1,-1),(1,1)]
    found = False
    for dr,dc in dirs:
        mr,mc = r+dr,c+dc
        lr,lc = r+dr*2,c+dc*2
        if not(0<=mr<8 and 0<=mc<8 and
              0<=lr<8 and 0<=lc<8): continue
        mp = state.board[mr][mc]
        lp = state.board[lr][lc]
        if mp and mp.player!=pc.player \
          and not lp and (lr,lc) not in path:
            find_caps(state,lr,lc,
                      path+[(lr,lc)],result)
            found = True
    if not found and len(path)>1:
        result.append(path)

def get_walks(state):
    walks,p = [],state.active
    dirs = [(-1,-1),(-1,1)] if p==0 \
          else [(1,-1),(1,1)]
    for r in range(8):
        for c in range(8):
            pc = state.board[r][c]
            if pc and pc.player==p:
                for dr,dc in dirs:
                    nr,nc = r+dr,c+dc
                    if 0<=nr<8 and 0<=nc<8 \
                      and not state.board[nr][nc]:
                        walks.append([(r,c),(nr,nc)])
    return walks