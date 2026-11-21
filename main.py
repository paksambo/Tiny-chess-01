import sys

P = {'P':100,'N':320,'B':330,'R':500,'Q':900,'K':20000}

def parse(fen):
    b=[]
    for r in fen.split()[0].split('/'):
        row=[]
        for c in r:
            if c.isdigit(): row.extend(['.']*int(c))
            else: row.append(c)
        b.append(row)
    return b, fen.split()[1] if len(fen.split())>1 else 'w'

def moves(b, t):
    m=[]
    d = {'N': [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],
         'B': [(-1,-1),(-1,1),(1,-1),(1,1)],
         'R': [(-1,0),(1,0),(0,-1),(0,1)],
         'Q': [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)],
         'K': [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]}
    for r in range(8):
        for c in range(8):
            p = b[r][c]
            if p=='.' or (p.isupper()!=(t=='w')): continue
            pt = p.upper()
            if pt=='P':
                dr = -1 if t=='w' else 1
                nr = r + dr
                if 0 <= nr < 8:
                    if b[nr][c]=='.':
                        m.append((r,c,nr,c))
                        if (t=='w' and r==6) or (t=='b' and r==1):
                            if b[r+2*dr][c]=='.': m.append((r,c,r+2*dr,c))
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < 8 and b[nr][nc]!='.' and b[nr][nc].isupper() != p.isupper():
                            m.append((r,c,nr,nc))
            elif pt in d:
                for dr, dc in d[pt]:
                    nr, nc = r+dr, c+dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        if b[nr][nc]=='.': m.append((r,c,nr,nc))
                        elif b[nr][nc].isupper() != p.isupper():
                            m.append((r,c,nr,nc)); break
                        else: break
                        if pt in 'NK': break
                        nr+=dr; nc+=dc
    return m

def uci(m):
    return 'abcdefgh'[m[1]] + str(8-m[0]) + 'abcdefgh'[m[3]] + str(8-m[2])

def ev(b):
    s = 0
    for row in b:
        for p in row:
            if p!='.':
                v = P.get(p.upper(),0)
                s += v if p.isupper() else -v
    return s

def search(b, d, a, beta, max_p):
    ms = moves(b, 'w' if max_p else 'b')
    if d==0 or not ms: return ev(b), None
    best = ms[0]
    if max_p:
        bv = -999999
        for m in ms:
            nb = [row[:] for row in b]
            nb[m[2]][m[3]] = nb[m[0]][m[1]]; nb[m[0]][m[1]] = '.'
            val, _ = search(nb, d-1, a, beta, False)
            if val > bv: bv, best = val, m
            a = max(a, val)
            if beta <= a: break
        return bv, best
    else:
        bv = 999999
        for m in ms:
            nb = [row[:] for row in b]
            nb[m[2]][m[3]] = nb[m[0]][m[1]]; nb[m[0]][m[1]] = '.'
            val, _ = search(nb, d-1, a, beta, True)
            if val < bv: bv, best = val, m
            beta = min(beta, val)
            if beta <= a: break
        return bv, best

def main():
    fen = sys.stdin.read().strip()
    if not fen: fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    b, t = parse(fen)
    _, best = search(b, 2, -999999, 999999, t=='w')
    ms = moves(b, t)
    print(uci(best) if best and best in ms else (uci(ms[0]) if ms else 'e2e4'))

if __name__=='__main__': main()
