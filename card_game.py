import numpy as np
import math
import random

class CardGame(object):
    def __init__(self, cards=np.array([0]*15)):
        '''
        Input:
            cards: (15) Numpy array, cards[i] corresponds to the number of certain card-face.
        '''
        self.cards = cards
        # self.statistics = self.get_statistics(self.cards)
        self.min_step_table = self.get_min_step_table()
    

    def get_statistics(self, cards):
        pass

    def get_min_step_table(self):
        F = np.ones((55,27,18,14)) * 54
        F[0][0][0][0] = 0
        for i in range(55):
            for j in range(27):
                for k in range(18):
                    for l in range(14):
                        if i + 2*j + 3*k + 4*l > 54: continue
                        if i:
                            F[i][j][k][l] = min(F[i][j][k][l], F[i-1][j][k][l]+1) # 1
                        if j:
                            F[i][j][k][l] = min(F[i][j][k][l], F[i][j-1][k][l]+1) # 2
                        if k:
                            F[i][j][k][l] = min(F[i][j][k][l], F[i][j][k-1][l]+1) # 3
                            if i:
                                F[i][j][k][l] = min(F[i][j][k][l],F[i-1][j][k-1][l]+1) # 3+1
                            if j:
                                F[i][j][k][l] = min(F[i][j][k][l],F[i][j-1][k-1][l]+1) # 3+2
                        if l:
                            F[i][j][k][l] = min(F[i][j][k][l],F[i][j][k][l-1]+1) # 4
                            if i >= 2:
                                F[i][j][k][l] = min(F[i][j][k][l],F[i-2][j][k][l-1]+1) # 4+1
                            if j >= 2:
                                F[i][j][k][l] = min(F[i][j][k][l],F[i][j-2][k][l-1]+1) # 4+2

        table = np.ones((15+1, 13+1, 13+1, 13+1)) * 54
        print(F[0][0][0][2])
        def s(x, y, z, w):
            if (y, z, w) == (0, 0, 0):
                return F[x][0][0][0]
            else:
                current_min = F[x][y][z][w]
                if w:
                    current_min = min(current_min, s(x+4, y, z, w-1), s(x+2, y+1, z, w-1), s(x+1, y, z+1, w-1), s(x, y+2, z, w-1))
                if z:
                    current_min = min(current_min, s(x+1, y+1, z-1, w), s(x+3, y, z-1, w))
                if y:
                    current_min = min(current_min, s(x+2, y-1, z, w))
                return current_min
        
        for x in range(15+1):
            for y in range(13+1):
                for z in range(13+1):
                    for w in range(13+1):
                        table[x][y][z][w] = s(x, y, z, w)
                        
        print(s(0,0,0,5))
                    

        





c = CardGame()