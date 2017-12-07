from keyboard import keyboard
import Tkinter as tk
from animation import Animation
import time

class mainApp(object):
    def __init__(self,margin,size,spacing,dt,options,hoverLimit = 4):
        self.hoverlimit = hoverLimit # after hovering hoverlimit time over a key, key is selected
        self.lastHoverTime = time.time() # record the time of a hovering on a key
        self.hoverDt = 0
        # mark which selection option is on(can be both on)
        self.clickOn = options[0]
        self.hoverOn = options[1]
        # record the last key mouse was hovering
        self.lastHoverKey = (-1,-1)
        #set up keyboard appearance and size Setting
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
        # data logging variables
        self.clickedKeys = [] # a list of clicked keys
        self.endIndex = [] # mark the end of a sequence of movement by index until a new key is selected
        self.mouseMovement = [] # a list of mouse position
        self.mouseMovementTime = [] # a list of corresponding time of mouse movement
        self.appStartTime = 0 # start time of the app(initialized in self.run())

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
    def movementLogging(self):
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        currentTime = time.time() - self.appStartTime
        self.mouseMovement.append((x,y))
        self.mouseMovementTime.append(currentTime)

    def endIndexLogging(self, keySelected):
        self.endIndex.append(len(self.mouseMovement)-1)
        self.clickedKeys.append(keySelected)


    def lightUpHovering(self):
        self.kb.turnOffAllHover()
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        keyIndex = self.hoveringKey(x,y)
        if keyIndex:
            self.kb.keys[keyIndex[0]][keyIndex[1]].hovering = 1


    def hoveringKey(self,x,y):
        for i in range(self.kb.row_len):
            for j in range(self.kb.col_len):
                (x0, x1, y0, y1) = (self.kb.keys[i][j].x0, self.kb.keys[i][j].x1,
                                    self.kb.keys[i][j].y0, self.kb.keys[i][j].y1)
                x_inrange = (x >= x0) and (x <= x1)
                y_inrange = (y >= y0) and (y <= y1)
                if (x_inrange and y_inrange):
                    return (i,j)
        return 0

    def clickEvent(self,event):
        (x, y) = (event.x, event.y)
        keyIndex = self.hoveringKey(x,y)
        if keyIndex:
            self.hoverDt = 0
            self.lastHoverKey = (-1, -1)
            (i,j) = keyIndex
            inputs = self.kb.keys[i][j].label
            if inputs == 'DEL' and self.inputText != 'INPUT:':
                self.inputText = self.inputText[:-1]
            elif inputs == ' ':
                self.inputText += '_'
            elif inputs != 'DEL':
                self.inputText += inputs
            self.endIndexLogging(inputs)


    def hoverSelect(self):
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        keyIndex = self.hoveringKey(x,y)
        if keyIndex:
            (i, j) = (keyIndex[0],keyIndex[1])
            if i == self.lastHoverKey[0] and j == self.lastHoverKey[1]:
                currentTime = time.time()
                dt = currentTime - self.lastHoverTime
                self.lastHoverTime = currentTime
                self.hoverDt += dt
                if self.hoverDt >= self.hoverlimit:
                    inputs = self.kb.keys[i][j].label
                    if inputs == 'DEL' and self.inputText != 'INPUT:':
                        self.inputText = self.inputText[:-1]
                    elif inputs == ' ':
                        self.inputText += '_'
                    elif inputs != 'DEL':
                        self.inputText += inputs
                    self.hoverDt = 0
                    self.lastHoverKey = (-1,-1)
                    self.endIndexLogging(inputs)
            else:
                self.lastHoverTime = time.time()
                self.lastHoverKey = (i,j)

    def saveData(self):
        fid = open('data.txt','w')
        counter = 0
        for i in range(len(self.mouseMovement)):
            move = self.mouseMovement[i]
            moveTime = self.mouseMovementTime[i]
            if counter >= len(self.endIndex): counter = len(self.endIndex)-1
            if i == self.endIndex[counter]:
                isEnd = 1
                symbol = self.clickedKeys[counter]
                counter += 1
            else:
                isEnd = 0
                symbol = 'NONE'
            if symbol == ' ': symbol = 'SP'
            fid.write('%f %f %f %s\n'%(move[0], move[1],moveTime,symbol))
        fid.close()





    def exitEvent(self):
        self.root.destroy()
        self.saveData()


    def run(self):
        self.root = tk.Tk()
        self.root.title('Keyboard Simulation')
        self.canvas = tk.Canvas(self.root, width=self.winWidth,
                             height=self.winHeight)
        self.canvas.pack()
        if self.clickOn:
            self.root.bind('<Button-1>',self.clickEvent)
        def timerFired():
            self.lightUpHovering()
            self.movementLogging()
            if self.hoverOn:
                self.hoverSelect()
            self.redrawAll()
            self.canvas.after(self.dt, timerFired)
        self.appStartTime = time.time()
        timerFired()
        self.root.protocol("WM_DELETE_WINDOW", self.exitEvent)
        self.root.mainloop()  # This call BLOCKS





if __name__ == '__main__':
    margin = (5,5)
    size = (60,60)
    spacing = (10,10)
    dt = 10
    options = (1,1)
    hoverLimit = 4
    myApp = mainApp(margin,size,spacing,dt,options,hoverLimit)
    myApp.run()

