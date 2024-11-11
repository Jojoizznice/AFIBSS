import pygame
import sys
import math

class Figuren:
    def __init__(self, screen, pos, identity, index):
        self.screen = screen
        self.pos = pos
        self.state = -1
        self.identity = identity
        self.color = (204,193,159) if self.identity == 'w' else (44,32,21)
        self.index = index

class Uisge:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Uisge")
        self.width, self.height = 7, 6
        self.screen = pygame.display.set_mode((self.width*64, self.height*64))
        self.clock = pygame.time.Clock()
        self.game_state = [
            ['','','','','',''],
            ['','','','w_3','',''],
            ['','','b_5','w_2','w_5',''],
            ['','b_1','b_4','w_1','w_4',''],
            ['','b_0','b_3','w_0','',''],
            ['','','b_2','','',''],
            ['','','','','','']
            ]
        self.pieces = []
        for j in range(len(self.game_state[0])):
            for i in range(len(self.game_state)-1, 0, -1):
                if self.game_state[i][j] != '':
                    self.pieces.append(Figuren(self.screen, (i,j), self.game_state[i][j][0], int(self.game_state[i][j][2])))
        self.turn = 'w'
        self.last_pressed = None
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.last_pressed:
                    if self.last_pressed.identity == 'b':
                        self.last_pressed.color = (44,32,21)
                    else:
                        self.last_pressed.color = (204,193,159)
                m_pos = pygame.mouse.get_pos()
                m_pos = [m_pos[0]//64, m_pos[1]//64]
                if self.game_state[m_pos[0]][m_pos[1]] != '':
                    if self.game_state[m_pos[0]][m_pos[1]][0] == self.turn:
                        if self.game_state[m_pos[0]][m_pos[1]][0] == 'b' and self.turn == 'b':
                            piece = self.pieces[int(self.game_state[m_pos[0]][m_pos[1]][2])]
                            piece.color = (90,80,67)
                        elif self.turn == 'w':
                            piece = self.pieces[int(self.game_state[m_pos[0]][m_pos[1]][2])+6]
                            piece.color = (161,148,119)
                        self.last_pressed = piece
                else:
                    if self.last_pressed:
                        if math.sqrt((m_pos[0]-self.last_pressed.pos[0])**2+(m_pos[1]-self.last_pressed.pos[1])**2) == 2:
                            
                            if self.game_state[self.last_pressed.pos[0]+int((m_pos[0]-self.last_pressed.pos[0])/2)][self.last_pressed.pos[1]+int((m_pos[1]-self.last_pressed.pos[1])/2)] != '':                       
                                res = self.rules_check(m_pos, self.last_pressed.pos)
                                self.last_pressed.pos = res[-1]
                                if self.last_pressed.pos == m_pos:                                    
                                    self.last_pressed.state *= -1
                                    self.last_pressed = None
                                    self.turn = 'b' if self.turn == 'w' else 'w'
                                if res[0]:
                                    print(res[1])
                                    pygame.quit()
                                    sys.exit()
                        elif self.last_pressed.state == 1:
                            if math.sqrt((m_pos[0]-self.last_pressed.pos[0])**2+(m_pos[1]-self.last_pressed.pos[1])**2) == 1 or math.sqrt((m_pos[0]-self.last_pressed.pos[0])**2+(m_pos[1]-self.last_pressed.pos[1])**2) == math.sqrt(2):
                                if self.game_state[m_pos[0]][m_pos[1]] == '':
                                    res = self.rules_check(m_pos, self.last_pressed.pos)
                                    self.last_pressed.pos = res[-1]
                                    if self.last_pressed.pos == m_pos:
                                        self.turn = 'b' if self.turn == 'w' else 'w' 
                                    self.last_pressed = None
                                    if res[0]:
                                        print(res[1])
                                        pygame.quit()
                                        sys.exit()
                        
    
    def rules_check(self, m_pos, last_pos):
        res = [last_pos]
        check = 0
        if len(self.game_state) > m_pos[0]+1:
                if self.game_state[m_pos[0]+1][m_pos[1]] != '' and self.game_state[m_pos[0]+1][m_pos[1]] != f'{self.last_pressed.identity}_{self.last_pressed.index}':
                    check += 1
        if check == 0 and 0 <= m_pos[0]-1:
            if self.game_state[m_pos[0]-1][m_pos[1]] != '' and self.game_state[m_pos[0]-1][m_pos[1]] != f'{self.last_pressed.identity}_{self.last_pressed.index}':
                check += 1
        if check == 0 and len(self.game_state[0]) > m_pos[1]+1:
            if self.game_state[m_pos[0]][m_pos[1]+1] != '' and self.game_state[m_pos[0]][m_pos[1]+1] != f'{self.last_pressed.identity}_{self.last_pressed.index}':
                check += 1
        if check == 0 and 0 <= m_pos[1]-1:
            if self.game_state[m_pos[0]][m_pos[1]-1] != '' and self.game_state[m_pos[0]][m_pos[1]-1] != f'{self.last_pressed.identity}_{self.last_pressed.index}':
                check += 1
        if check == 0:
            pass
        else:
            res[0] = m_pos
            save = self.game_state[last_pos[0]][last_pos[1]]
            self.game_state[last_pos[0]][last_pos[1]] = ''
            self.game_state[m_pos[0]][m_pos[1]] = save
            
        if check != 0:
            for piece in self.pieces:
                if check != 0:
                    check = 0
                    if len(self.game_state) > piece.pos[0]+1:
                            if self.game_state[piece.pos[0]+1][piece.pos[1]] != '':
                                check += 1
                    if check == 0 and 0 <= piece.pos[0]-1:
                        if self.game_state[piece.pos[0]-1][piece.pos[1]] != '':
                            check += 1
                    if check == 0 and len(self.game_state[0]) > piece.pos[1]+1:
                        if self.game_state[piece.pos[0]][piece.pos[1]+1] != '':
                            check += 1
                    if check == 0 and 0 <= piece.pos[1]-1:
                        if self.game_state[piece.pos[0]][piece.pos[1]-1] != '':
                            check += 1
                    if check == 0:
                        res[0] = last_pos
                        self.game_state[m_pos[0]][m_pos[1]] = ''
                        self.game_state[last_pos[0]][last_pos[1]] = save
                        break
                    else:
                        res[0] = m_pos
        check = 0

        self.check_connection()

        for i in range((len(self.pieces)//2)):
            if self.pieces[i].state == 1:
                check += 1
            else:
                res.insert(0, '')
                res.insert(0, False)
                return res
            if check == 6:
                res.insert(0, 'Black wins')
                res.insert(0, True)
                return res    
        check = 0
        for i in range((len(self.pieces)//2), len(self.pieces)):
            if self.pieces[i].state == 1:
                check += 1
            else:
                res.insert(0, '')
                res.insert(0, False)
                return res
            if check == 6:
                res.insert(0, 'White wins')
                res.insert(0, True)
                return res     

    def check_connection(self):
        check = [['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','','']]   # same as self.game_state
        
        first: int = self.get_first_field(self.game_state)

        (firstR, firstW) = self.int_to_pos(first)

        check[firstR][firstW] = '0' # first piece is placed in array

        poslist: list[int] = [first]
        
        while True:
            if len(poslist) == 0:
                break

            if ([5, 11, 17, 23, 19, 35, 41].__contains__(poslist[0]) == False): #exclude right out of bounds 
                self.connection_mover(poslist[0], 1, poslist, check) # checking all 4 dirs
            if ([0, 6, 12, 18, 24, 30, 36].__contains__(poslist[0]) == False): #exclude left out of bounds 
                self.connection_mover(poslist[0], -1, poslist, check)

            if (poslist[0] < 36): #exclude right out of bounds 
                self.connection_mover(poslist[0], 6, poslist, check)
            if (poslist[0] > 5): #exclude left out of bounds 
                self.connection_mover(poslist[0], -6, poslist, check)
            poslist.remove(poslist[0])
        
        ctr = 0
        for row in check:
            for piece in row:
                if (piece != ''):
                    ctr += 1

        if (ctr != 12):
            print("check failed")
            
        
    def connection_mover(
            self,
            pos: int, 
            dir: int, 
            poslist: list[int], 
            check: list[list[str]]): # dir must be 1, -1, 6 or -6
    
        if ([1, -1, 6, -6].__contains__(dir) == -1):
            raise ValueError(f"internal error in check_connection, was {dir}")

        pos += dir
        (r, w) = self.int_to_pos(pos)

        if (self.game_state[r][w] != '' and check[r][w] != '0'): # check if piece placed and not already there
            check[r][w] = '0'
            poslist.append(pos) # needs further check



    @staticmethod             
    def pos_to_int(row, width):
        return 6 * row + width
    
    @staticmethod
    def int_to_pos(pos):
        r = int(pos / 6) # row from top
        w = pos - 6 * int(pos / 6) # width from right
        return (r, w)
        
    def get_first_field(self, arr: list[list[str]]):
        ctr = 0
        for row in arr:
            for piece in row:
                if piece != '':
                    return ctr
                ctr += 1

    def run(self):
        while True:
            self.screen.fill((60, 60, 60))
            for i in range(self.width):
                pygame.draw.line(self.screen, (200, 200, 200), (i*64, 0), (i*64, self.height*64))
            for i in range(self.height):
                pygame.draw.line(self.screen, (200, 200, 200), (0, i*64), (self.width*64, i*64))
            for piece in self.pieces:
                pygame.draw.circle(self.screen, piece.color, (piece.pos[0]*64+32, piece.pos[1]*64+32), 24)
                if piece.state == 1:
                    pygame.draw.circle(self.screen, (0,0,0), (piece.pos[0]*64+32, piece.pos[1]*64+32), 12)
            self.move()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    main = Uisge()
    main.run()