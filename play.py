import random
from tkinter.constants import GROOVE, RAISED, RIDGE, SUNKEN
from typing import Text
import tkinter as tk
from PIL import Image, ImageTk
import os, sys
import numpy as np
from dfs_play import CardGame as Game1
from copy import deepcopy

os.chdir(sys.path[0])
path=sys.path[0]
if os.path.isfile(path):
    path=os.path.split(path)[0]


class MainWindow(object):
    _minWidth, _minHeight = 1280, 720
    _marginX, _marginY, _marginC = 30, 30, 21
    _cardX, _cardY = 100, 140

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chinese Poker")
        self.window.minsize(self._minWidth, self._minHeight)
        self.cards = np.array([0] * 15)
        self.card_imgs = []
        self.selected_idx = set()
        self.init_components()
        self.window.mainloop()

    def init_components(self):
        self.canvas = tk.Canvas(self.window,
                        # bg="white",
                        width=self._minWidth,
                        height=self._minHeight)
        self.canvas.pack()
        self.canvas.place(relx=0, rely=0)
        
        for i in range(54):
            self.card_imgs.append(ImageTk.PhotoImage(
                    (Image.open(f'resource/pokers/{i+1}.png')).resize((self._cardX, self._cardY))
                    ))
            self.canvas.create_image((self._marginX + self._marginC*i, self._marginY), anchor='nw', image=self.card_imgs[i])
        
        self.button1 = tk.Button(self.window, text="Solve 1", padx=1, pady=1, command=self.solve_1)
        self.button1.place(x=self._marginX, y=(self._marginY+20+self._cardY))

        self.canvas.bind('<Button-1>', self.clickCanvas)
        print('success initial display.')


    def get_statistics(self):
        for i in self.selected_idx:
            self.cards[self.idx2cardValue(i)] += 1
        print(f'cards distribution: {self.cards}')


    def solve_1(self):
        print('starting to solve 1')
        self.get_statistics()
        game1 = Game1(cards=self.cards)
        game1.solve_game()
        self.display_solution(game1.current_best_solution)

    def display_solution(self, solution):
        x = self._marginX
        y = self._marginY + self._cardY + 70
        idxs = deepcopy(self.selected_idx)
        for i in range(1,len(solution)): # i 出的手牌手数
            print(solution[i])
            for j in range(len(solution[i])): # j 0-14
                if (j == 13 or j == 14) and solution[i][j] and j + 39 in idxs:
                    idxs.remove(j+39)
                    self.canvas.create_image((x, y), anchor='nw', image=self.card_imgs[j + 39])
                    x += self._marginC
                else:
                    count = solution[i][j]
                    # print(count)
                    while count:
                        count -= 1
                        for idx in [4*j, 4*j+1, 4*j+2, 4*j+3]:
                            if idx in idxs:
                                # print(self.idx2cardName(idx))
                                idxs.remove(idx)
                                self.canvas.create_image((x, y), anchor='nw', image=self.card_imgs[idx])
                                x += self._marginC
                                break
            x += self._cardX + self._marginC


    def idx2cardValue(self, i):
        if i < 52: return int(i / 4)
        elif i == 52: return 13
        elif i == 53: return 14
    
    def idx2cardName(self, i):
        if i == 52: return 'Black Joker'
        elif i == 53: return 'Red Joker'
        else:
            value = self.idx2cardValue(i)
            remain = i % 4
            if value <= 7: str1 = f"{value+3}"
            elif value == 8: str1 = 'J'
            elif value == 9: str1 = 'Q'
            elif value == 10: str1 = 'K'
            elif value == 11: str1 = 'A'
            elif value == 12: str1 = '2'
            if remain == 0: str2 = 'spade'
            elif remain == 1: str2 = 'diamond'
            elif remain == 2: str2 = 'heart'
            elif remain == 3: str2 = 'club'
            return str1 + ' of ' + str2


    def select_card_i(self, i):
        if i in self.selected_idx:
            self.selected_idx.remove(i)
            print(f'remove {self.idx2cardName(i)}')
            self.canvas.delete(f'box_{i}')
        else:
            self.selected_idx.add(i)
            print(f'select {self.idx2cardName(i)}')
            self.canvas.create_rectangle(self._marginX+i*self._marginC,
                self._marginY,
                self._cardX+self._marginX+i*self._marginC if i == 53 else self._marginX+(i+1)*self._marginC,
                self._marginY+self._cardY,
                outline='green', width=5, tag=f'box_{i}')


    def clickCanvas(self, event):
        point = (event.x, event.y)
        if (point[1] > self._marginY
            and point[1] < self._marginY + self._cardY
            and point[0] > self._marginX
            and point[0] < self._marginX + self._marginC * 53 + self._cardX):
            i = min(53, int((point[0] - self._marginX) / self._marginC))
            self.select_card_i(i)



if __name__ == '__main__':
    MainWindow()