import numpy as np
import random
from copy import deepcopy


def in_limit(my_cards, cards_to_play):
    '''用来判断是否可以出这个手牌。'''
    return (min(my_cards - cards_to_play) >= 0)


def get_possible_plays(my_cards):
    possible_plays = []
    # 三顺子
    for i in range(2, 12): # 连续的3个的组数
        for j in range(0, 13-i):
            play = np.array([0]*j + [3]*i + [0]*(15-i-j))
            if in_limit(my_cards, play):
                possible_plays.append((play, f'3*{i}', j))
    # 间隔三顺子
    for i in range(2, 6):
        for j in range(0, 14-2*i):
            play = np.array([0]*j + [3,0,]*i + [0]*(15-2*i-j))
            if in_limit(my_cards, play):
                possible_plays.append((play, f'3^{i}', j))
    # 双顺子
    for i in range(3, 12): # 连续的对子的组数
        for j in range(0, 13-i):
            play = np.array([0]*j + [2]*i + [0]*(15-i-j))
            if in_limit(my_cards, play):
                possible_plays.append((play, f'2*{i}', j))
    # 间隔双顺子
    for i in range(3, 6):
        for j in range(0, 14-2*i):
            play = np.array([0]*j + [2,0,]*i + [0]*(15-2*i-j))
            if in_limit(my_cards, play):
                possible_plays.append((play, f'2^{i}', j))
    # 单顺子
    for i in range(5, 12): # TODO
        for j in range(0, 13-i):
            play = np.array([0]*j + [1]*i + [0]*(15-i-j))
            if in_limit(my_cards, play):
                possible_plays.append((play, f'1*{i}', j))
    # 间隔单顺子
    for i in [5, 6]:
        for j in range(0, 14-2*i):
            play = np.array([0]*j + [1,0,]*i + [0]*(15-2*i-j))
            if in_limit(my_cards, play):
                possible_plays.append((play, f'1^{i}', j))
    # 四带二对
    for i in range(0,13): # 4
        for j in range(0,12): # 2-1
            if j == i: continue
            for k in range(j+1,13): # 2-2
                if k == i: continue
                play = np.array([0]*15)
                play[i] = 4
                play[j] = 2
                play[k] = 2
                if in_limit(my_cards, play):
                    possible_plays.append((play, '4+2+2', i))
    # 四带二
    for i in range(0,13):
        for j in range(0,13):
            if j == i: continue
            play = np.array([0]*15)
            play[i] = 4
            play[j] = 2
            if in_limit(my_cards, play):
                possible_plays.append((play, '4+2', i))
    # 三带二
    for i in range(0,13):
        for j in range(0,13):
            if j == i: continue
            play = np.array([0]*15)
            play[i] = 3
            play[j] = 2
            if in_limit(my_cards, play):
                possible_plays.append((play, '3+2', i))
    # 三带一
    for i in range(0,13):
        for j in range(0,13):
            if j == i: continue
            play = np.array([0]*15)
            play[i] = 3
            play[j] = 1
            if in_limit(my_cards, play): possible_plays.append((play, '3+1', i))
    # 炸弹
    for i in range(0,13):
        play = np.array([0]*15)
        play[i] = 4
        if in_limit(my_cards, play): possible_plays.append((play, '4', i))
    # 三张牌
    for i in range(0,13):
        play = np.array([0]*15)
        play[i] = 3
        if in_limit(my_cards, play): possible_plays.append((play, '3', i))
    # 2
    for i in range(0,13):
        play = np.array([0]*15)
        play[i] = 2
        if in_limit(my_cards, play): possible_plays.append((play, '2', i))
    # 1
    for i in range(0,15):
        play = np.array([0]*15)
        play[i] = 1
        if in_limit(my_cards, play): possible_plays.append((play, '1', i))
    # 火箭
    if in_limit(my_cards, np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1])): possible_plays.append((np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]), 'rocket', 13))
    if len(possible_plays) == 0:
        possible_plays.append((np.array([0]*15), 'null', -1))
        return possible_plays
    possible_plays.sort(key=lambda x: -(sum(x[0])*3-x[2])) # 先出小牌和张数多的牌
    possible_plays = possible_plays[:20]
    return possible_plays



class Judger(object):
    def __init__(self, ANum=20, BNum=20):
        self.ANum = ANum
        self.BNum = BNum
        self.Acards = np.array([0] * 15)
        self.Bcards = np.array([0] * 15)
        self.played_cards = np.array([0] * 15)
        self.init_hand_out()
        self.game_on = True
    
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
    
    def A_play(self, Adecision):
        print(f'A plays: {Adecision}, remains {self.Acards}')
        self.Acards -= Adecision[0]
        self.played_cards += Adecision[0]
        if sum(self.Acards) == 0:
            print('A wins')
            self.game_on = False

    def B_play(self, Bdecision):
        print(f'B plays: {Bdecision}, remains {self.Bcards}')
        self.Bcards -= Bdecision[0]
        self.played_cards += Bdecision[0]
        if sum(self.Bcards) == 0:
            print('B wins')
            self.game_on = False


class Player(object):
    def __init__(self, cards):
        self.cards = deepcopy(cards) # [0,0,0,0,0,2,0,4,0,0,0,0,0,1,1]
        self.played_cards = np.array([0] * 15)
        self.unknown_cards = np.array([4] * 13 + [1, 1]) - cards
    
    def play(self, last, format, value):
        '''
        last 上次对手出牌。
        format: string, n+m/1*5,2*3,3*2/1^5,2^3,3^2/4+2+2
        value: n+m，则为n；顺子，则为顺子开头。
        '''
        # update
        self.unknown_cards -= last
        self.played_cards += last
        options = self.get_options(self.cards, format, value)
        decision = options[0]
        self.cards -= decision[0]
        self.played_cards += decision[0]
        return decision


    def get_options(self, hand_cards, format, value):
        my_cards = hand_cards
        options = []
        # play
        if format == 'null':
            return get_possible_plays(hand_cards)
        elif format == 'rocket':
            pass
        elif format == '4+2+2':
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
        if len(options) == 0:
            options.append((np.array([0]*15), 'null', -1))
        options.sort(key=lambda x: x[2])
        return options


if __name__ == '__main__':
    judger = Judger()
    A = Player(judger.Acards)
    B = Player(judger.Bcards)
    Bdecision = (np.array([0]*15), 'null', -1)
    while judger.game_on:
        Adecision = A.play(*Bdecision)
        judger.A_play(Adecision)
        if not judger.game_on: break
        Bdecision = B.play(*Adecision)
        judger.B_play(Bdecision)
