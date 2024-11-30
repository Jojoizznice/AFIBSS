import pygame
import pygame.freetype
import sys
import math
import time, threading
import copy
import uisgeai

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
        self.pWisAI, self.pBIsAI, = False, True
        self.wAI = ""
        self.bAI = uisgeai.UisgeAi(False)
        self.width, self.height = 7, 6
        self.screen = pygame.display.set_mode((self.width*64, self.height*64))
        self.game_font = pygame.freetype.Font(file=None, size=24)
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
        self.pre_game_state = self.game_state.copy()
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
            
            if (self.turn == 'w' and self.pWisAI):
                self.wAI.move(self.get_position())
                pass
            elif (self.turn == 'b' and self.pBIsAI):
                self.bAI.move(self.get_position())
                pass

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
                    return
                
                if not self.last_pressed:
                    return
                if math.sqrt((m_pos[0]-self.last_pressed.pos[0])**2+(m_pos[1]-self.last_pressed.pos[1])**2) == 2:
                    
                    if self.game_state[self.last_pressed.pos[0]+int((m_pos[0]-self.last_pressed.pos[0])/2)][self.last_pressed.pos[1]+int((m_pos[1]-self.last_pressed.pos[1])/2)] != '':                       
                        res = self.rules_check(m_pos, self.last_pressed.pos)
                        self.last_pressed.pos = res[-1]
                        if self.last_pressed.pos == m_pos:                                    
                            self.last_pressed.state *= -1
                            self.turn = 'b' if self.turn == 'w' else 'w'
                            self.last_pressed = None
                        if res[0]:
                            print(res[1])
                            pygame.quit()
                            sys.exit()
                    return
                
                if self.last_pressed.state == 1:
                    if not (math.sqrt((m_pos[0]-self.last_pressed.pos[0])**2+(m_pos[1]-self.last_pressed.pos[1])**2) == 1 or math.sqrt((m_pos[0]-self.last_pressed.pos[0])**2+(m_pos[1]-self.last_pressed.pos[1])**2) == math.sqrt(2)):
                        return
                    if self.game_state[m_pos[0]][m_pos[1]] != '':
                        return
                    res = self.rules_check(m_pos, self.last_pressed.pos)
                    self.last_pressed.pos = res[-1]
                    if self.last_pressed.pos == m_pos:
                        self.turn = 'b' if self.turn == 'w' else 'w' 
                        self.last_pressed = None
                    if res[0]:
                        print(res[1])
                        pygame.quit()
                        sys.exit()
                    return
                        
    
    def rules_check(self, m_pos, last_pos):
        res = [last_pos]
        check = 0
        save = self.game_state[last_pos[0]][last_pos[1]]
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
            self.game_state[last_pos[0]][last_pos[1]] = ''
            self.game_state[m_pos[0]][m_pos[1]] = save

        if check == 0 or not self.check_connection():
            res[0] = last_pos
            res.append(False)
            self.game_state[m_pos[0]][m_pos[1]] = ''
            self.game_state[last_pos[0]][last_pos[1]] = save
        else:
            res.append(True)
            res[0] = m_pos

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

            if ([5, 11, 17, 23, 29, 35, 41].__contains__(poslist[0]) == False): #exclude right out of bounds 
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
            self.game_state = self.pre_game_state
            return False
        return True     
        
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

    def get_position(self) -> str:
        poslist: list[list[Figuren]] = [[None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6]
#        for i in range(7):
#            for k in range(6):
#                poslist[i][k] = i

        for piece in self.pieces:
            pos = piece.pos
            poslist[pos[0]][pos[1]] = piece

        posstr = ""
        for row in poslist:
            for piece in row:
                if piece == None:
                    posstr += '0'
                    continue
                p = piece.identity
                if(piece.state == 1):
                    p = p.capitalize()
                posstr += p
            posstr += "/"

        return posstr + " " + self.turn
    
    def get_legal_moves(self):
        pre_game_state = copy.deepcopy(self.game_state)
        moves = []
        for piece in self.pieces:
            self.last_pressed = piece
            if piece.identity != self.turn:
                continue

            if piece.pos[1]+2 < len(self.game_state[0]):
                if self.rules_check((piece.pos[0], piece.pos[1]+2), piece.pos)[-1] == True:
                    moves.append(((piece.pos[0], piece.pos[1]+2), piece.index))
                self.game_state = copy.deepcopy(pre_game_state)
            if piece.pos[1]-2 >= 0:
                if self.rules_check((piece.pos[0], piece.pos[1]-2), piece.pos)[-1] == True:
                    moves.append(((piece.pos[0], piece.pos[1]-2), piece.index))
                self.game_state = copy.deepcopy(pre_game_state)
            if piece.pos[0]+2 < len(self.game_state):
                if self.rules_check((piece.pos[0]+2, piece.pos[1]), piece.pos)[-1] == True:
                    moves.append(((piece.pos[0]+2, piece.pos[1]), piece.index))
                self.game_state = copy.deepcopy(pre_game_state)
            if piece.pos[0]-2 >= 0:
                if self.rules_check((piece.pos[0]-2, piece.pos[1]), piece.pos)[-1] == True:
                    moves.append(((piece.pos[0]-2, piece.pos[1]), piece.index))
                self.game_state = copy.deepcopy(pre_game_state)

            if piece.state != 1: #Now get altnernate legal moves for promoted pieces
                continue
            if piece.pos[1]+1 < len(self.game_state[0]) and piece.pos[0]-1 >= 0:
                if self.rules_check((piece.pos[0]-1, piece.pos[1]+1), piece.pos)[-1] == True:
                    moves.append(((piece.pos[0]-1, piece.pos[1]+1), piece.index))
                self.game_state = copy.deepcopy(pre_game_state)
            if piece.pos[1]+1 < len(self.game_state[0]) and piece.pos[0]+1 < len(self.game_state):
                if self.rules_check((piece.pos[0]+1, piece.pos[1]+1), piece.pos)[-1] == True:
                    moves.append(((piece.pos[0]+1, piece.pos[1]+1), piece.index))
                self.game_state = copy.deepcopy(pre_game_state)
            if piece.pos[1]-1 >= 0 and piece.pos[0]+1 < len(self.game_state):
                if self.rules_check((piece.pos[0]+1, piece.pos[1]-1), piece.pos)[-1] == True:
                    moves.append(((piece.pos[0]+1, piece.pos[1]-1), piece.index))
                self.game_state = copy.deepcopy(pre_game_state)
            if piece.pos[1]-1 >= 0 and piece.pos[0]-1 >= 0:
                if self.rules_check((piece.pos[0]-1, piece.pos[1]-1), piece.pos)[-1] == True:
                    moves.append(((piece.pos[0]-1, piece.pos[1]-1), piece.index))
                self.game_state = copy.deepcopy(pre_game_state)

        print(moves)
        return moves
    
    def show_index(self): #For debugging (shows index of pieces in pieces array in UI)
        for piece in self.pieces:
            self.game_font.render_to(self.screen, (piece.pos[0]*64+20, piece.pos[1]*64+20), f'{piece.index}')


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
                    return ctr #searches for first piece
                ctr += 1

    def initialise(self):
        self.screen.fill((60, 60, 60))
        for i in range(self.width):
            pygame.draw.line(self.screen, (200, 200, 200), (i*64, 0), (i*64, self.height*64))
        for i in range(self.height):
            pygame.draw.line(self.screen, (200, 200, 200), (0, i*64), (self.width*64, i*64))
        for piece in self.pieces:
            pygame.draw.circle(self.screen, piece.color, (piece.pos[0]*64+32, piece.pos[1]*64+32), 24)
            if piece.state == 1:
                pygame.draw.circle(self.screen, (0,0,0), (piece.pos[0]*64+32, piece.pos[1]*64+32), 12)

    def update(self):
        pygame.display.update()
        self.clock.tick(60)

    def run(self):
        while True:
            self.initialise()
            self.get_legal_moves()
            self.show_index() #For debugging (shows index of pieces in pieces array in UI)
            self.move()
            self.update()

if __name__ == '__main__':
    main = Uisge()
    main.run()
