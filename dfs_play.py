# DFS search for least round solution
# AI project 1.1

import random
import numpy as np
import time
import argparse
from queue import Queue
import copy

class CardGame(object):
    def __init__(self, cards=None, N=0):
        '''
        Input:
            cards: (15) Numpy array, cards[i] corresponds to the number of certain card-face.
        '''
        if cards == None:
            self.my_cards = self.initialize(N)
        else:
            self.my_cards = cards
        self.max_min_depth = 54 # 目前搜索到最短的出牌方式。不会比着出牌更多了。
        self.current_best_solution = [] # 目前搜索的最好出牌方式。
        self.current_path = ['init',]
        # self.closed = set() # close set. All explored
        # self.print_info = [] # list of dic {'card': list of cards, 'policy': string e.g.'四带二'}
        # self.policy_list = [] # list of dic {'step': step, 'score': score}
    

    def initialize(self, N):
        '''random initialize my cards, count = N
        
        Input:
            - N: number of cards
            
        Output:
            - cards: np array (15) [4 4 4 4 4 4 4 4 4 4 4 4 4 1 1]
        '''
        assert N <= 54 and N > 0, "N must be positive int smaller than 54"
        cards = np.array([0] * 15)
        for x in random.sample(range(0, 54), N):
            if x == 53:
                cards[14] = 1
            else:
                cards[x//4] += 1
        return cards

    def done(self):
        return sum(self.my_cards) == 0

    def play_cards(self, cards_to_play):
        my_cards_after = self.my_cards - cards_to_play
        assert min(my_cards_after) >= 0, "invalid play!"
        self.current_path.append(cards_to_play)
        self.my_cards = my_cards_after

    def restore_cards(self, cards_to_restore):
        self.current_path.pop()
        self.my_cards = self.my_cards + cards_to_restore

    def in_limit(self, cards_to_play):
        '''用来判断是否可以出这个手牌。'''
        return (min(self.my_cards - cards_to_play) >= 0)

    def get_possible_plays(self):
        possible_plays = []
        S = sum(self.my_cards)
        if S >= 6:
            # 三顺子
            for i in range(2, 12): # 连续的3个的组数
                for j in range(0, 13-i):
                    play = np.array([0]*j + [3]*i + [0]*(15-i-j))
                    if self.in_limit(play): possible_plays.append(play)
            # 间隔三顺子
            for i in range(2, 6):
                for j in range(0, 14-2*i):
                    play = np.array([0]*j + [3,0,]*i + [0]*(15-2*i-j))
                    if self.in_limit(play): possible_plays.append(play)
            # 双顺子
            for i in range(3, 12): # 连续的对子的组数
                for j in range(0, 13-i):
                    play = np.array([0]*j + [2]*i + [0]*(15-i-j))
                    if self.in_limit(play): possible_plays.append(play)
            # 间隔双顺子
            for i in range(3, 6):
                for j in range(0, 14-2*i):
                    play = np.array([0]*j + [2,0,]*i + [0]*(15-2*i-j))
                    if self.in_limit(play): possible_plays.append(play)
        if S >= 5:
            # 单顺子
            for i in range(5, 12): # TODO
                for j in range(0, 13-i):
                    play = np.array([0]*j + [1]*i + [0]*(15-i-j))
                    if self.in_limit(play): possible_plays.append(play)
            # 间隔单顺子
            for play in [np.array([1,0,1,0,1,0,1,0,1,0,0,0,0,0,0]),
                        np.array([0,1,0,1,0,1,0,1,0,1,0,0,0,0,0]),
                        np.array([0,0,1,0,1,0,1,0,1,0,1,0,0,0,0]),
                        np.array([0,0,0,1,0,1,0,1,0,1,0,1,0,0,0]),
                        np.array([1,0,1,0,1,0,1,0,1,0,1,0,0,0,0]),
                        np.array([0,1,0,1,0,1,0,1,0,1,0,1,0,0,0])]:
                if self.in_limit(play): possible_plays.append(play)
        if S >= 8:
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
                        if self.in_limit(play): possible_plays.append(play)
        if S >= 6:
            # 四带二
            for i in range(0,13):
                for j in range(0,13):
                    if j == i: continue
                    play = np.array([0]*15)
                    play[i] = 4
                    play[j] = 2
                    if self.in_limit(play): possible_plays.append(play)
        if S >= 5:
        # 三带二
            for i in range(0,13):
                for j in range(0,13):
                    if j == i: continue
                    play = np.array([0]*15)
                    play[i] = 3
                    play[j] = 2
                    if self.in_limit(play): possible_plays.append(play)
        if S >= 4:
            # 三带一
            for i in range(0,13):
                for j in range(0,13):
                    if j == i: continue
                    play = np.array([0]*15)
                    play[i] = 3
                    play[j] = 1
                    if self.in_limit(play): possible_plays.append(play)
            # 炸弹
            for i in range(0,13):
                play = np.array([0]*15)
                play[i] = 4
                if self.in_limit(play): possible_plays.append(play)
        if S >= 3:
            # 三张牌
            for i in range(0,13):
                play = np.array([0]*15)
                play[i] = 3
                if self.in_limit(play): possible_plays.append(play)
        if S >= 2:
            # 2
            for i in range(0,13):
                play = np.array([0]*15)
                play[i] = 2
                if self.in_limit(play): possible_plays.append(play)
            # 火箭
            if self.in_limit(np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1])): possible_plays.append(np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]))
        # 1
        for i in range(0,15):
            play = np.array([0]*15)
            play[i] = 1
            if self.in_limit(play): possible_plays.append(play)
        possible_plays.sort(key=lambda x: -sum(x))
        return possible_plays

    def dfs(self, depth):
        if self.done():
            if depth < self.max_min_depth:
                self.max_min_depth = depth
                self.current_best_solution.clear()
                self.current_best_solution = copy.deepcopy(self.current_path)
            return
        possible_plays = self.get_possible_plays()
        for this_play in possible_plays:
            if sum(self.my_cards) > (self.max_min_depth - depth - 1) * sum(this_play): break # 如果按照现在这种出法，无法提前一次，则不必继续搜索
            # print(f'{self.my_cards} - {this_play} - {depth}')
            self.play_cards(this_play)
            self.dfs(depth + 1)
            self.restore_cards(this_play)
    
    def solve_game(self):
        print(f'initialization: {list(self.my_cards)}')
        self.dfs(0)
        print(f'done! depth = {self.max_min_depth}, path =  {self.current_best_solution}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='number of cards', type=int, default=20)
    parser.add_argument('-c', help='list of cards', type=list, default=None)
    opt = parser.parse_args()
    tic = time.time()
    game = CardGame(N=opt.n, cards=opt.c)
    game.solve_game()