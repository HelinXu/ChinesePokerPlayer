# BFS search for least round solution
# AI project 1.1

import random
import numpy as np
import time
import argparse
from queue import Queue

def initialize(N):
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


def card_hash(cards):
    s = sum(cards)
    for i in cards:
        s = s * 10 + i
    return s

def play_cards(my_cards, cards_to_play):
    my_cards_after = my_cards - cards_to_play
    assert min(my_cards_after) >= 0, "invalid play!"
    return my_cards_after


def in_limit(my_cards, cards_to_play):
    '''用来判断是否可以出这个手牌。'''
    return (min(my_cards - cards_to_play) >= 0)


def get_possible_plays(my_cards, hash_upper):
    max_min_step = sum(my_cards != np.zeros(my_cards.shape))
    ave_num = sum(my_cards) / max_min_step# 几次一定可以出完？不能出得比这少！
    # print(ave_num)
    possible_plays = []
    # 三顺子
    for i in range(2, 12): # 连续的3个的组数
        for j in range(0, 13-i):
            play = np.array([0]*j + [3]*i + [0]*(15-i-j))
            if in_limit(my_cards, play):
                possible_plays.append(play)
    # 间隔三顺子
    for i in range(2, 6):
        for j in range(0, 14-2*i):
            play = np.array([0]*j + [3,0,]*i + [0]*(15-2*i-j))
            if in_limit(my_cards, play):
                possible_plays.append(play)
    # 双顺子
    for i in range(3, 12): # 连续的对子的组数
        for j in range(0, 13-i):
            play = np.array([0]*j + [2]*i + [0]*(15-i-j))
            if in_limit(my_cards, play):
                possible_plays.append(play)
    # 间隔双顺子
    for i in range(3, 6):
        for j in range(0, 14-2*i):
            play = np.array([0]*j + [2,0,]*i + [0]*(15-2*i-j))
            if in_limit(my_cards, play):
                possible_plays.append(play)
    # 单顺子
    for i in range(5, 12): # TODO
        for j in range(0, 13-i):
            play = np.array([0]*j + [1]*i + [0]*(15-i-j))
            if in_limit(my_cards, play):
                possible_plays.append(play)
    # 间隔单顺子
    for play in [np.array([1,0,1,0,1,0,1,0,1,0,0,0,0,0,0]),
                np.array([0,1,0,1,0,1,0,1,0,1,0,0,0,0,0]),
                np.array([0,0,1,0,1,0,1,0,1,0,1,0,0,0,0]),
                np.array([0,0,0,1,0,1,0,1,0,1,0,1,0,0,0]),
                np.array([1,0,1,0,1,0,1,0,1,0,1,0,0,0,0]),
                np.array([0,1,0,1,0,1,0,1,0,1,0,1,0,0,0])]:
        if in_limit(my_cards, play):
            possible_plays.append(play)
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
                    possible_plays.append(play)
    # 四带二
    for i in range(0,13):
        for j in range(0,13):
            if j == i: continue
            play = np.array([0]*15)
            play[i] = 4
            play[j] = 2
            if in_limit(my_cards, play):
                possible_plays.append(play)
    # 三带二
    for i in range(0,13):
        for j in range(0,13):
            if j == i: continue
            play = np.array([0]*15)
            play[i] = 3
            play[j] = 2
            if in_limit(my_cards, play):
                possible_plays.append(play)
    # 三带一
    for i in range(0,13):
        for j in range(0,13):
            if j == i: continue
            play = np.array([0]*15)
            play[i] = 3
            play[j] = 1
            if in_limit(my_cards, play): possible_plays.append(play)
    # 炸弹
    for i in range(0,13):
        play = np.array([0]*15)
        play[i] = 4
        if in_limit(my_cards, play): possible_plays.append(play)
    # 三张牌
    for i in range(0,13):
        play = np.array([0]*15)
        play[i] = 3
        if in_limit(my_cards, play): possible_plays.append(play)
    # 2
    for i in range(0,13):
        play = np.array([0]*15)
        play[i] = 2
        if in_limit(my_cards, play): possible_plays.append(play)
    # 1
    for i in range(0,15):
        play = np.array([0]*15)
        play[i] = 1
        if in_limit(my_cards, play): possible_plays.append(play)
    # 火箭
    if in_limit(my_cards, np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1])): possible_plays.append(np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]))
    possible_plays_tmp = []
    for play in possible_plays:
        if card_hash(play) <= hash_upper and len(play) >= ave_num: possible_plays_tmp.append(play)
    possible_plays_tmp.sort(key=lambda x: -card_hash(x))
    return possible_plays_tmp



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='number of cards', type=int, default=20)
    opt = parser.parse_args()
    tic = time.time()
    upper = 1e18
    cards = initialize(opt.n)
    q = Queue()
    q.put((cards, 0, upper))
    while not q.empty():
        v = q.get()
        neighbors = get_possible_plays(v[0], v[2])
        # print(len(neighbors))
        num = v[1]
        for play in neighbors:
            v2 = play_cards(v[0], play)
            if (max(v2) == 0): 
                print(f'Done! {num}')
                toc = time.time()
                print(toc - tic)
            q.put((v2, num + 1, card_hash(play)))

