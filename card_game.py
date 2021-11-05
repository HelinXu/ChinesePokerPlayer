import numpy as np

class CardGame(object):
    def __init__(self, cards=np.array([0]*15)):
        '''
        Input:
            cards: (15) Numpy array, cards[i] corresponds to the number of certain card-face.
        '''
        self.cards = cards
        self.closed = set() # close set. All explored
        self.print_info = [] # list of dic {'card': list of cards, 'policy': string e.g.'四带二'}
        self.policy_list = [] # list of dic {'step': step, 'score': score}


    def get_min_step_table(self):
        '''
        动态规划方法：速查表的构建
        '''
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
