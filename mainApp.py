from keyboard import keyboard
import Tkinter as tk
from animation import Animation

class mainApp(object):
    def __init__(self,margin,size,spacing,dt):
        self.backgroundColor = 'black'
        self.keyColor = 'white'
        self.hoverColor = 'cyan'
        self.textHeight = 200
        self.inputText = 'INPUT:'
        self.kb = keyboard(size,spacing,self.keyColor,self.hoverColor,(margin[0],margin[1] + self.textHeight))
        self.widthMargin = margin[0]
        self.heightMargin = margin[1]
        self.winWidth = self.kb.width + 2* self.widthMargin
        self.winHeight = self.kb.height + 2*self.heightMargin+self.textHeight
        self.dt = dt

####################################################################### start of drawing section
    def drawBackground(self):
        self.canvas.create_rectangle(0,0,self.winWidth,self.winHeight,
                                     fill = self.backgroundColor)

    def drawText(self):
        self.canvas.create_text(self.winWidth/2,self.textHeight/2, text = self.inputText,fill = 'white')

    def redrawAll(self):
        self.canvas.delete(tk.ALL)
        self.drawBackground()
        self.kb.draw(self.canvas)
        self.drawText()

######################################################################### end of drawing section
    def lightUpHovering(self):
        self.kb.turnOffAllHover()
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        for i in range(self.kb.row_len):
            for j in range(self.kb.col_len):
                (x0,x1,y0,y1) = (self.kb.keys[i][j].x0, self.kb.keys[i][j].x1,
                                 self.kb.keys[i][j].y0, self.kb.keys[i][j].y1)
                x_inrange = (x >= x0) and (x <= x1)
                y_inrange = (y >= y0) and (y <= y1)
                if (x_inrange and y_inrange):
                    self.kb.keys[i][j].hovering = 1
                    return 0
    def clickEvent(self,event):
        (x, y) = (event.x, event.y)
        for i in range(self.kb.row_len):
            for j in range(self.kb.col_len):
                (x0, x1, y0, y1) = (self.kb.keys[i][j].x0, self.kb.keys[i][j].x1,
                                    self.kb.keys[i][j].y0, self.kb.keys[i][j].y1)
                x_inrange = (x >= x0) and (x <= x1)
                y_inrange = (y >= y0) and (y <= y1)
                if (x_inrange and y_inrange):
                    inputs = self.kb.keys[i][j].label
                    if inputs == 'DEL' and self.inputText != 'INPUT:':
                        self.inputText = self.inputText[:-1]
                    elif inputs == ' ':
                        self.inputText += '_'
                    elif inputs != 'DEL':
                        self.inputText += inputs



    def run(self):
        self.root = tk.Tk()
        self.root.title('Keyboard Simulation')
        self.canvas = tk.Canvas(self.root, width=self.winWidth,
                             height=self.winHeight)
        self.canvas.pack()
        self.root.bind('<Button-1>',self.clickEvent)
        def timerFired():
            self.lightUpHovering()
            self.redrawAll()
            self.canvas.after(self.dt, timerFired)
        timerFired()
        self.root.mainloop()  # This call BLOCKS





if __name__ == '__main__':
    margin = (5,5)
    size = (60,60)
    spacing = (10,10)
    dt = 10
    myApp = mainApp(margin,size,spacing,dt)
    myApp.run()

