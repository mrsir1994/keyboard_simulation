#from tkFileDialog import askopenfilename
import string
import numpy as np
from scipy import interpolate
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import pickle

def data2List():
    fileDir = 'data.txt'
    fileObj = open(fileDir,'r')
    fileStrings = map(string.split,fileObj.readlines())
    (pos, t, cha) = ([[],[]],[],[])
    for line in fileStrings:
        pos[0].append(float(line[0]))
        pos[1].append(float(line[1]))
        t.append(float(line[2]))
        cha.append(line[3])
    print len(cha)
    return (pos,t,cha)

def getChaT(cha,t):
    newCha = []
    chaT = []
    for i in range(len(cha)):
        if cha[i] != 'NONE':
            newCha.append(cha[i])
            chaT.append(t[i])
    return (newCha,chaT)


def smoothData(pos,t,dt):
    windowSize = 3
    order = 2
    pos = [np.array(pos[0]),np.array(pos[1])]
    old_t = t
    t = np.array(t)
    newx = interpolate.interp1d(t, pos[0],kind = 'cubic')
    newy = interpolate.interp1d(t, pos[1],kind = 'cubic')
    pos2 = [[],[]]
    pos2[0] = savgol_filter(pos[0],5,4)
    pos2[1] = savgol_filter(pos[1], 5, 4)
    t2 = savgol_filter(t,5,2)

    newtime = np.linspace(old_t[0], old_t[-1],int((old_t[-1]-old_t[0])/dt))
    pos[0] = newx(newtime)
    pos[1] = newy(newtime)

    return (pos,newtime,pos2,t2)

def list2Dict(pos,t,cha,chaT):
    dList = []
    counter = 0
    last_i = 0
    for i in range(len(t)):
        if counter >= len(cha): break
        if t[i] >= chaT[counter]:
            d = dict()
            d['x'] = pos[0][last_i:i]
            d['y'] = pos[1][last_i:i]
            d['t'] = t[last_i:i]
            d['char'] = cha[counter]
            dList.append(d)
            last_i = i
            counter += 1


    output = open('myfile.pkl', 'wb')
    pickle.dump(dList, output)
    output.close()






if __name__ == '__main__':
    (pos, t, cha) = data2List()
    old_pos = pos
    (newCha, chaT) = getChaT(cha,t)
    old_t = t
    (pos,t,pos2,t2) = smoothData(pos, t, 1/1000.0)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(pos[0], pos[1], 'green', label='interpolated')
    #ax.plot(pos2[0],pos2[1],'b', label='smoothed')
    ax.plot(old_pos[0],old_pos[1],'r.',label = 'uninterpolated')
    ax.plot()
    list2Dict(pos,t,newCha,chaT)

    plt.show()

