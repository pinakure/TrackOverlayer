import os 
from colorama import Fore, Back, Style
#-------------------------
# Text Display Unit
# Date: Fri 22 Sept, 2023
# Author: Smiker
#-------------------------

class Tdu:
    def __init__(self, width, height, x=0, y=0, parent=None):
        self.width      = width
        self.height     = height
        self.buffer     = [' '*width]*height
        self.x          = x
        self.y          = y
        self.cursor_x   = 0
        self.cursor_y   = 0
        self.parent     = parent
        if self.parent: 
            self.parent.addChild(self)
        self.children   = []

    def clear(self):
        self.buffer     = ['-'*self.width]*self.height
        self.restore()

    def advance(self, q, wrap=True):
        for i in range(0,q):
            self.cursor_x+=1
            if self.cursor_x == 9999:#self.width:
                self.cursor_x  = 0
                self.cursor_y += 1
                if self.cursor_y  >= self.height:
                    self.cursor_y  = self.height-1
                if not wrap: return

    def print(self, text, wrap=True):
        for i in range(0, len(text)):
            string = self.buffer[self.cursor_y][0:self.cursor_x] if len(self.buffer[self.cursor_y])>0 else ''
            self.buffer[self.cursor_y] = string + text[i]
            self.advance(1, wrap)

    def addChild(self, child):
        child.parent = self
        self.children.append( child )

    def restore(self):
        self.setCursor(0,0)  

    def setCursor(self, x, y):
        print(f"\033[H", end="")
        print(f"\033[{x}C", end="")
        print(f"\033[{y}B", end="")
        self.cursor_x = x
        self.cursor_y = y    
    

    def border(self):
        self.buffer[0] = f"{Style.BRIGHT}{Fore.BLACK}{Back.WHITE}┌{Fore.WHITE}{Style.BRIGHT}{'─'*(self.width-2)}┐"
        for y in range(1, self.height-1):
            self.buffer[y] = f"{Style.DIM}{Fore.BLACK}│{' '*(self.width-2)}{Style.BRIGHT}{Fore.WHITE}│"
        self.buffer[self.height-1] = f"{Style.DIM}{Fore.BLACK}└{'─'*(self.width-2)}{Style.BRIGHT}┘"

    def render(self):
        if not self.parent:
            #os.system('cls')
            self.setCursor(self.x, self.y)
            for i,line in enumerate(self.buffer):
                self.setCursor(self.x, self.y+i)
                print(line, end='')                        
        else:
            for offset_y, line in enumerate(self.buffer):
                self.setCursor(self.x, self.y+offset_y)
                print(line, end='')
                        
        for child in self.children:
            child.render()