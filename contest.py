import numpy as np
import random
from copy import deepcopy
class Judger(object):
    def __init__(self, ANum=20, BNum=20):
        self.ANum = ANum
        self.BNum = BNum
        self.Acards = np.array([0] * 15)
        self.Bcards = np.array([0] * 15)
        self.played_cards = np.array([0] * 15)
        self.init_hand_out()

    
    def init_hand_out(self):
        '''hand out cards!'''
        rand_choice = random.sample(range(0, 54), self.ANum + self.BNum)
        for x in rand_choice[0:self.ANum]:
            if x == 53:
                self.Acards[14] = 1
            else:
                self.Acards[x//4] += 1
        for x in rand_choice[self.ANum:]:
            if x == 53:
                self.Bcards[14] = 1
            else:
                self.Bcards[x//4] += 1
    
    def in_limit(self, cards_to_play, hand_cards):
        '''this cards in limit of hand cards'''
        return (min(hand_cards - cards_to_play) >= 0)
    

    def larger_cards(self, this, last):
        '''this cards > last cards (comparable and larger)'''
        if last[13] == last[14] == 1:
            # 双王
            return False
        a = [0, 0, 0, 0, 0] # 0,1,2,3,4; blackj, redj
        b = [0, 0, 0, 0, 0] # 0,1,2,3,4; blackj, redj
        for i in range(15):
            a[this[i]] += 1
            b[last[i]] += 1
        print(this, a, last, b)
        if (a == b == [14, 1, 0, 0, 0]):
            pass
        if a != b:
            return False



    def check_valid_input(self, this_cards, last_cards, hand_cards):
        '''
        1) this cards > last cards (comparable and larger)
        2) this cards in limit of hand cards
        '''


    def get_a_input(self, cards):
        pass


class Player(object):
    def __init__(self, cards):
        self.cards = cards # [0,0,0,0,0,2,0,4,0,0,0,0,0,1,1]
        self.played_cards = np.array([0] * 15)
        self.unknown_cards = np.array([4] * 13 + [1, 1]) - cards
    
    def read_last(self, last, format, value):
        '''
        last 上次对手出牌。
        format: string, n+m/1*5,2*3,3*2/1^5,2^3,3^2/4+2+2
        value: n+m，则为n；顺子，则为顺子开头。
        '''
        # update
        self.unknown_cards -= last
        self.played_cards += last
        my_cards = deepcopy(self.cards)
        options = []
        # play
        if format == '4+2+2':
            for i in range(value+1,15):
                if self.cards[i] == 4:
                    my_cards[i] = 0
                    for j in range(13):
                        if j == i: continue
                        # print(my_cards[j], j)
                        if my_cards[j] >= 2:
                            for k in range(j+1, 13):
                                if my_cards[k] >= 2:
                                    tmp = np.array([0]*15)
                                    tmp[i] = 4
                                    tmp[j] = 2
                                    tmp[k] = 2
                                    options.append((tmp, format, i))
                    my_cards[i] = 4
        elif len(format) == 1:
            # n+0
            main_count = int(format[0]) # 1,2,3,4
            for i in range(value+1,15):
                if self.cards[i] >= main_count:
                    tmp = np.array([0]*15)
                    tmp[i] = main_count
                    options.append((tmp, format, i))
        elif format[1] == '+':
            # n+m
            main_count = int(format[0]) # 1,2,3,4
            for i in range(value+1,15):
                if self.cards[i] >= main_count:
                    my_cards[i] -= main_count
                    for j in range(15):
                        if j == i: continue
                        # print(my_cards[j], j)
                        if my_cards[j] >= int(format[2:]):
                            tmp = np.array([0]*15)
                            tmp[i] = main_count
                            tmp[j] = int(format[2:])
                            options.append((tmp, format, i))
                    my_cards[i] += main_count
        elif format[1] == '*':
            # x*m
            length = int(format[2:])
            for i in range(value+1, 13-length):
                for j in range(i, i+length):
                    if my_cards[j] < int(format[0]): break
                else:
                    tmp = np.array([0]*15)
                    for j in range(i, i+length): tmp[j] = int(format[0])
                    options.append((tmp, format, i))
        elif format[1] == '^':
            length = int(format[2:])
            for i in range(value+1, 14-length*2):
                for j in range(i, i+length*2, 2):
                    if my_cards[j] < int(format[0]): break
                else:
                    tmp = np.array([0]*15)
                    for j in range(i, i+length*2, 2): tmp[j] = int(format[0])
                    options.append((tmp, format, i))           
        
        print(options)



if __name__ == '__main__':
    j = Judger()
    j.larger_cards(np.array([0,0,0,0,0,2,0,4,0,0,0,0,0,1,1]),np.array([0,0,4,0,0,0,0,0,0,0,0,2,0,1,1]))
    p = Player(np.array([1,4,2,0,0,2,0,0,1,0,3,0,4,1,1]))
    p.read_last(np.array([0,0,0,0,0,1,0,4,0,0,0,0,0,1,0]), '4+2+2', 1)