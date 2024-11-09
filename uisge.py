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
                    print(i,j, self.game_state[i][j], self.game_state[j][i])
                    self.pieces.append(Figuren(self.screen, (i,j), self.game_state[i][j][0], int(self.game_state[i][j][2])))
                    print(int(self.game_state[i][j][2]))
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
                print(m_pos)
                if self.game_state[m_pos[0]][m_pos[1]] != '':
                    
                    if self.game_state[m_pos[0]][m_pos[1]][0] == 'b':
                        piece = self.pieces[int(self.game_state[m_pos[0]][m_pos[1]][2])]
                        print(piece.pos, self.game_state[piece.pos[0]][piece.pos[1]])
                        piece.color = (90,80,67)
                    else:
                        piece = self.pieces[int(self.game_state[m_pos[0]][m_pos[1]][2])+6]
                        piece.color = (161,148,119)
                    self.last_pressed = piece

                    if piece.state == 1:
                        pass
                else:
                    if self.last_pressed:
                        print(math.sqrt((m_pos[0]-self.last_pressed.pos[0])**2+(m_pos[1]-self.last_pressed.pos[1])**2))
                        if math.sqrt((m_pos[0]-self.last_pressed.pos[0])**2+(m_pos[1]-self.last_pressed.pos[1])**2) == 2:
                            
                            if self.game_state[self.last_pressed.pos[0]+int((m_pos[0]-self.last_pressed.pos[0])/2)][self.last_pressed.pos[1]+int((m_pos[1]-self.last_pressed.pos[1])/2)] != '':
                                self.game_state[m_pos[0]][m_pos[1]] = self.game_state[self.last_pressed.pos[0]][self.last_pressed.pos[1]]
                                self.game_state[self.last_pressed.pos[0]][self.last_pressed.pos[1]] = ''
                                print(self.game_state)
                                print(self.game_state[self.last_pressed.pos[0]][self.last_pressed.pos[1]], self.game_state[m_pos[0]][m_pos[1]])
                                self.last_pressed.pos = m_pos
                                self.last_pressed.state *= -1
                                print(self.last_pressed.state)
                                self.last_pressed = None
                    
    
    def rules(self, m_pos):
        pass        

    def run(self):
        while True:
            self.screen.fill((60, 60, 60))
            for i in range(self.width):
                pygame.draw.line(self.screen, (200, 200, 200), (i*64, 0), (i*64, self.height*64))
            for i in range(self.height):
                pygame.draw.line(self.screen, (200, 200, 200), (0, i*64), (self.width*64, i*64))
            for piece in self.pieces:
                pygame.draw.circle(self.screen, piece.color, (piece.pos[0]*64+32, piece.pos[1]*64+32), 24)
            self.move()
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    main = Uisge()
    main.run()
