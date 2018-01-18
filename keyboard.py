from Tkinter import *
#from  import askdirectory, askopenfilename
import string
import numpy as np

class keyboard(object):
    def __init__(self,size,spacing,keyColor,hoverColor,margin):

        # ask the dir of the keyboardfile
        #kbDir = askopenfilename()
        #print kbDir
        kbFile = open('KB','r')
        kbStrings = kbFile.readlines() # read in string
        self.convertKbToArray(kbStrings) #convert string to 2-d list

        # number of rows and cols in the keyboard
        self.col_len = len(self.kbArray[0])
        self.row_len = len(self.kbArray)
        # the width and height of one cell on the keyboard
        self.cell_width = size[0]
        self.cell_height = size[1]
        # the spacing between cells on board
        self.col_spacing = spacing[0]
        self.row_spacing = spacing[1]
        # size of the entire board (cell size + spacing)
        self.width = (self.cell_width + self.col_spacing) * self.col_len - self.col_spacing
        self.height =(self.cell_height + self.row_spacing) * self.row_len - self.row_spacing
        self.keyColor = keyColor
        self.hoverColor = hoverColor
        self.margin = margin


        self.getCellPosition()
        self.constructKeys()




    def convertKbToArray(self, kbStrings): # convert the read-in data to numpy.array
        self.kbArray = []
        for line in kbStrings:
            new_row = []
            for item in string.split(line):
                if item == 'SP':
                    new_row.append(' ')
                    continue
                new_row.append(item)
            self.kbArray.append(new_row)



    def getCellPosition(self): # calculate the position of each key in the window
        row_counter = np.array(range(0,self.row_len))
        col_counter = np.array(range(0,self.col_len))
        row_spacing = self.cell_height + self.row_spacing
        col_spacing = self.cell_width + self.col_spacing

        a = np.meshgrid(col_counter * col_spacing,row_counter * row_spacing)
        self.row_pos = a[1]
        self.col_pos = a[0]

    def constructKeys(self): # create and store key instances
        self.keys = []
        for i in range(self.row_len):
            new_row = []
            for j in range(self.col_len):
                y0 = self.row_pos[i][j]
                x0 = self.col_pos[i][j]
                y1 = y0 + self.cell_height
                x1 = x0 + self.cell_width
                label = self.kbArray[i][j]

                new_row.append(key(x0,y0,x1,y1,self.keyColor,self.hoverColor,label,self.margin))
            self.keys.append(new_row)

    def turnOffAllHover(self): # turn off all the light up effect
        for i in range(self.row_len):
            for j in range(self.col_len):
                self.keys[i][j].hovering = 0

    def draw(self,canvas): # draw the keys in the window
        for i in range(self.row_len):
            for j in range(self.col_len):
                self.keys[i][j].draw(canvas)





class key(object): # class of the keys
    def __init__(self,x0,y0,x1,y1,color,hoverColor,label,margin):
        self.x_margin = margin[0]
        self.y_margin = margin[1]
        self.label = label
        self.x0 = x0 + self.x_margin
        self.y0 = y0 + self.y_margin
        self.x1 = x1 + self.x_margin
        self.y1 = y1 + self.y_margin
        self.color = color
        self.hoverColor = hoverColor
        self.hovering = 0
    def draw(self,canvas):
        if self.hovering:
            color = self.hoverColor
        else:
            color = self.color
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill = color)
        canvas.create_text((self.x0+self.x1)/2.0,(self.y0+self.y1)/2.0,text = self.label)



if __name__ == "__main__":
    kb = keyboard((1,2),(2,3))
    print (kb.kbArray)
    print (kb.row_len,kb.col_len)
    print (kb.row_pos)
    print (kb.col_pos)