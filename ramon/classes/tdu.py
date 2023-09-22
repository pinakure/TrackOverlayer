import os 
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
        self.x          = 0
        self.y          = 0
        self.cursor_x   = 0
        self.cursor_y   = 0
        self.parent     = None
        self.children   = []

    def advance(self, q, wrap=True):
        for i in range(0,q):
            self.cursor_x+=1
            if self.cursor_x == self.width:
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
        self.cursor_x = 0
        self.cursor_y = 0    

    def render(self):
        for child in self.children:
            child.render()

        if not self.parent:
            os.system('cls')
            for line in self.buffer:
                print(line, end='')
        else:
            for offset_y, line in enumerate(self.buffer):
                self.parent.cursor_x = self.x
                self.parent.cursor_y = self.y+offset_y
                self.parent.print(line, wrap=False)