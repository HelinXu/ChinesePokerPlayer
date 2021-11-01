import random
from tkinter.constants import GROOVE, RAISED, RIDGE, SUNKEN
from typing import Text
import tkinter as tk
from PIL import Image, ImageTk
import os, sys
import numpy as np

os.chdir(sys.path[0])
path=sys.path[0]
if os.path.isfile(path):
    path=os.path.split(path)[0]


class MainWindow(object):
    _minWidth, _minHeight = 1280, 720
    card_imgs = []
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chinese Poker")
        self.window.minsize(self._minWidth, self._minHeight)
        self.cards = np.array([0] * 15)
        # self.card_imgs = []
        self.init_card_display()
        self.window.mainloop()

    def init_card_display(self):
        self.canvas = tk.Canvas(self.window,
                        bg="white",
                        width=self._minWidth,
                        height=self._minHeight)
        self.canvas.place(relx=0, rely=0)
        
        for i in range(54):
            self.card_imgs.append(ImageTk.PhotoImage(Image.open(f'resource/pokers/{i+1}.png')))
            self.canvas.create_image((30 + 21*i, 30), anchor='nw', image=self.card_imgs[i])
        print('success initial display.')


if __name__ == '__main__':
    MainWindow()