from keyboard import keyboard
import Tkinter as tk
from Tkinter import Scrollbar,Text,RIGHT,LEFT,Y,END,Spinbox,Label,Entry, StringVar
from animation import Animation
import time
import ttk
import argparse
import os
from time import gmtime, strftime,localtime

class mainApp(object):
    def __init__(self,margin,size,spacing,dt,options,hoverLimit = 4,save_dir = ''):

        self.save_dir = save_dir
        self.uid = os.getuid
        self.uname = os.getlogin()
        self.timemark = strftime("%a, %d %b %Y %H:%M:%S", localtime())




        self.hoverlimit = hoverLimit # after hovering hoverlimit time over a key, key is selected
        self.lastHoverTime = time.time() # record the start of hovering on a key
        self.hoverDt = 0 # record how long the mouse is hovering on a key
        # mark which selection option is on(can be both on)
        self.clickOn = options[0] # 1 for click mode on
        self.hoverOn = options[1] # 1 for hover mode on
        # record the last key mouse was hovering
        self.lastHoverKey = (-1,-1)
        #set up keyboard appearance and size Setting
        self.backgroundColor = 'black'
        self.keyColor = 'white'
        self.hoverColor = 'cyan'
        self.textHeight = 0
        self.inputText = 'INPUT:'
        self.kb = keyboard(size,spacing,self.keyColor,self.hoverColor,(margin[0],margin[1] + self.textHeight))
        self.widthMargin = margin[0]
        self.heightMargin = margin[1]
        self.winWidth = self.kb.width + 2* self.widthMargin
        self.winHeight = self.kb.height + 2*self.heightMargin+self.textHeight
        # the time interval the whole app is running at
        self.dt = dt
        # data logging variables
        self.clickedKeys = [] # a list of clicked keys
        self.endIndex = [] # mark the end of a sequence of movement by index until a new key is selected
        self.mouseMovement = [] # a list of mouse position
        self.mouseMovementTime = [] # a list of corresponding time of mouse movement
        self.appStartTime = 0 # start time of the app(initialized in self.run())
        # record if cap is turned on or not
        self.cap = True

####################################################################### start of drawing section
    def drawBackground(self):
        self.canvas.create_rectangle(0,0,self.winWidth,self.winHeight,
                                     fill = self.backgroundColor)

    def drawText(self): # draw the text on each key
        self.canvas.create_text(self.winWidth/2,self.textHeight/2, text = self.inputText,fill = 'white')

    def redrawAll(self): # redraw everything in window to create animation
        self.canvas.delete(tk.ALL)
        self.drawBackground()
        self.kb.draw(self.canvas)
        #self.drawText()

######################################################################### end of drawing section
    def movementLogging(self): # record the position of mouse and time of the position
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        currentTime = time.time() - self.appStartTime
        self.mouseMovement.append((x,y))
        self.mouseMovementTime.append(currentTime)

    def endIndexLogging(self, keySelected): # record the key selected
        self.endIndex.append(len(self.mouseMovement)-1)
        self.clickedKeys.append(keySelected)


    def lightUpHovering(self): # check if mouse is on a key to light the key up
        self.kb.turnOffAllHover()
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        keyIndex = self.hoveringKey(x,y)
        if keyIndex:
            self.kb.keys[keyIndex[0]][keyIndex[1]].hovering = 1
    def flipKeyCases(self):
        for i in range(self.kb.row_len):
            for j in range(self.kb.col_len):
                label = self.kb.keys[i][j].label
                if label != 'CAP' and label != 'DEL' and label != 'SP' :
                    if self.cap:
                        label = label.upper()
                    else:
                        label = label.lower()
                self.kb.keys[i][j].label = label

    def hoveringKey(self,x,y): # check which key the mouse is hovering on
        for i in range(self.kb.row_len):
            for j in range(self.kb.col_len):
                (x0, x1, y0, y1) = (self.kb.keys[i][j].x0, self.kb.keys[i][j].x1,
                                    self.kb.keys[i][j].y0, self.kb.keys[i][j].y1)
                x_inrange = (x >= x0) and (x <= x1)
                y_inrange = (y >= y0) and (y <= y1)
                if (x_inrange and y_inrange):
                    return (i,j)
        return 0

    def clickEvent(self,event): # when mouse clicked, check if it selected a key and record it
        if not self.clickOn: return
        (x, y) = (event.x, event.y)
        keyIndex = self.hoveringKey(x,y)
        if keyIndex:
            self.hoverDt = 0
            self.lastHoverKey = (-1, -1)
            self.progress["value"] = 0
            (i,j) = keyIndex
            inputs = self.kb.keys[i][j].label
            if inputs == 'CAP':
                self.cap = not self.cap
                self.flipKeyCases()
            elif inputs == 'DEL' and self.inputText != 'INPUT:':
                self.inputText = self.inputText[:-1]
            elif inputs == ' ':
                self.inputText += '_'
            elif inputs != 'DEL':
                if self.cap: inputs = inputs.upper()
                else: inputs = inputs.lower()
                self.inputText += inputs
            self.T.delete(1.0,END)
            self.T.insert(END,self.inputText)
            self.T.see(END)
            self.endIndexLogging(inputs)


    def hoverSelect(self): # if mouse hovers on a key more than threshold, then the key is selected
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
                    if inputs == 'CAP':
                        self.cap = not self.cap
                        self.flipKeyCases()
                    elif inputs == 'DEL' and self.inputText != 'INPUT:':
                        self.inputText = self.inputText[:-1]
                    elif inputs == ' ':
                        self.inputText += '_'
                    elif inputs != 'DEL':
                        if self.cap:
                            inputs = inputs.upper()
                        else:
                            inputs = inputs.lower()
                        self.inputText += inputs
                    self.hoverDt = 0
                    self.lastHoverKey = (-1,-1)
                    self.progress["value"] = 0
                    self.T.delete(1.0, END)
                    self.T.insert(END, self.inputText)
                    self.T.see(END)
                    self.endIndexLogging(inputs)
            elif(keyIndex == 0):
                self.hoverDt = 0
                self.lastHoverKey = (-1, -1)
                self.progress["value"] = 0
            else:
                self.hoverDt = 0
                self.lastHoverKey = (-1, -1)
                self.progress["value"] = 0
                self.lastHoverTime = time.time()
                self.lastHoverKey = (i,j)

    def saveData(self): # save all the data inside a file
        save_dir = self.save_dir + '/data_' + self.timemark + '_@_' + self.uname + '.txt'
        fid = open(save_dir,'w')
        counter = 0
        for i in range(len(self.mouseMovement)):
            move = self.mouseMovement[i]
            moveTime = self.mouseMovementTime[i]
            if counter >= len(self.endIndex): counter = len(self.endIndex)-1
            if counter == -1: break
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
        self.root3.destroy()
        self.root2.destroy()


    def run(self): # run the whole app
        self.root = tk.Tk()
        self.root2 = tk.Tk()
        self.root3 = tk.Tk()
        self.root.title('Keyboard Simulation')

        # keyboard setup
        self.canvas = tk.Canvas(self.root, width=self.winWidth,
                             height=self.winHeight)
        self.canvas.pack(side=LEFT)

        #
        self.S = Scrollbar(self.root2)
        self.T = Text(self.root2, height=4, width=50)


        self.S.pack(side=RIGHT, fill=Y,expand=True)
        self.T.pack(side=LEFT, fill=Y,expand=True)
        #self.S.pack()
        #self.T.pack()

        self.S.config(command=self.T.yview)
        self.T.config(yscrollcommand=self.S.set)
        self.T.delete(1.0, END)
        self.T.insert(END, self.inputText)
        self.T.see(END)


        l = Label(self.root3, text="Hover time Limit:",state = 'disabled')
        l.pack()

        w = Spinbox(self.root3, from_=0, to=10)
        w.pack()
        w.delete(0, "end")
        w.insert(0, 4)

        l2 = Label(self.root3, text="Hover select progress:")
        l2.pack()

        self.progress = ttk.Progressbar(self.root3, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress["value"] = 0
        self.progress["maximum"] = 10



        self.progress.pack()


        def hv_toggle():
            if self.hv_btn.config('text')[-1] == "Hover Select: On":
                self.hv_btn.config(text = "Hover Select: off")
                self.hoverOn = not self.hoverOn
            else:
                self.hv_btn.config(text ="Hover Select: On" )
                self.hoverOn = not self.hoverOn

        self.hv_btn = tk.Button(self.root3, text="Hover Select: On", command=hv_toggle)
        self.hv_btn.pack()


        def ck_toggle():
            if self.ck_btn.config('text')[-1] == "Click Select: On":
                self.ck_btn.config(text = "Click Select: off")
                self.clickOn = not self.clickOn
            else:
                self.ck_btn.config(text ="Click Select: On" )
                self.clickOn = not self.clickOn

        self.ck_btn = tk.Button(self.root3, text="Click Select: On", command=ck_toggle)
        self.ck_btn.pack()









        #self.hoverlimit = int(w.get())
        if self.clickOn:
            self.root.bind('<Button-1>',self.clickEvent)
        def timerFired():
            try:
                self.hoverlimit = int(w.get())
            except:
                pass

            self.progress["value"] = self.progress["maximum"] * self.hoverDt / self.hoverlimit


            self.lightUpHovering()
            self.movementLogging()
            if self.hoverOn:
                self.hoverSelect()
            self.redrawAll()
            self.canvas.after(self.dt, timerFired)
        self.appStartTime = time.time()
        timerFired()
        self.root.protocol("WM_DELETE_WINDOW", self.exitEvent)
        self.root2.protocol("WM_DELETE_WINDOW", self.exitEvent)
        self.root3.protocol("WM_DELETE_WINDOW", self.exitEvent)
        self.root.mainloop()  # This call BLOCKS
        self.root2.mainloop()
        self.root3.mainloop()





if __name__ == '__main__':
    #parser = argparse.ArgumentParser()
   # parser.add_argument("save_dir",help = 'the directory to save data')
   # args = parser.parse_args()





    margin = (5,5)
    size = (60,60)
    spacing = (10,10)
    dt = 10
    options = (1,1) # add toggle
    hoverLimit = 4
    #data_save_dir = args.save_dir
    #print data_save_dir, type(data_save_dir)
    myApp = mainApp(margin,size,spacing,dt,options,hoverLimit,'data')
    myApp.run()

