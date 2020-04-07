import PySimpleGUI as sg
import os
from playsound import playsound
from matplotlib import pyplot as plt
import numpy as np


FIG_H, FIG_W = 500, 500
# make up some data in the interval ]0, 1[
y = np.random.normal(loc=0.5, scale=0.4, size=1000)
y = y[(y > 0) & (y < 1)]
y.sort()
x = np.arange(len(y))

# plot with various axes scales
plt.figure(1)

plt.plot(x, y)
plt.yscale('linear')
plt.title('linear')
plt.grid(True)

plt.show()


sg.theme('Dark Black') 
ls = os.listdir("/home/ljkeller/code/python/pybeats/54__sleep__guitar/")
ls.sort()
ls = list(filter(lambda f: f.endswith(".wav"), ls))
# All this inside window
layout = [    [sg.Text("Lets get started making beats")],
              [sg.Listbox(ls, size=(30, 8), key='-File Path-')],
              [sg.Text("What file do you want to modify?")],
              [sg.Input(size=(45,1)), sg.FileBrowse(file_types=(("ALL Files", "*.wav"),))],
              [sg.Button('Play'), sg.Button('Cancel')]]

# Create the window
win_name = "Py Beats (" + os.getcwd() + ")"
window = sg.Window(win_name, layout)
# Event loop to process events
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    if event == "Play":
        if values['-File Path-']:
            #print(os.getcwd() + "/54__slee__guitar/" + values['-File Path-'][0])
            playsound(os.getcwd() + "/54__sleep__guitar/" + values['-File Path-'][0])
        else:
            fpath = values[0]
            playsound(fpath)
            print(event)
            print('You entered ', values[0])

