import uisge

class UisgeAi:
    def __init__(self, isWhite: bool):
        self.isWhite = isWhite

    def move(self, posstr: str, time = -1) -> tuple[tuple[int, int], tuple[int, int]]:
        
        pos: list[list[uisge.Figuren]] = [[None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6]
        for i in range(7):
            for k in range(6):
                pos[i][k] = i

        posarr = str.split(str(posstr), '/')
        i = 0
        for row in posarr:
            k = 0
            for l in row:
                if l == ' ':
                    posarr.clear()
                    break
                if l.isnumeric():
                    pos[i][k] = 0
                else: 
                    pos[i][k] = l
                k += 1
            i += 1
        
        self.get_legal_moves(pos)


        return None
    
    def get_legal_moves(self, pos: list[list[uisge.Figuren]]):
        s = 4
        del s

if __name__ == '__main__':
    main = uisge.Uisge()
    main.run()
