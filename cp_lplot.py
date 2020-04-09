#!/usr/bin/env python
import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import wave
"""
Demonstrates one way of embedding Matplotlib figures into a PySimpleGUI window.

Paste your Pyplot code into the section marked below.

Do all of your plotting as you normally would, but do NOT call plt.show(). 
Stop just short of calling plt.show() and let the GUI do the rest.

The remainder of the program will convert your plot and display it in the GUI.
If you want to change the GUI, make changes to the GUI portion marked below.

"""

# ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE -------------------------------

wd = os.getcwd() + "/"
if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    exit(1)

signal = wave.open(wd + fname, mode='rb')
fs = signal.getframerate()
signal = np.frombuffer(signal.readframes(-1), dtype="int16")
n_signal = signal.size

t = np.linspace(0, n_signal / fs, num=n_signal)

fourier_coeffs = np.fft.rfft(signal)
omegas = np.fft.rfftfreq(n_signal, 1./fs)

plt.figure()
plt.plot(omegas, fourier_coeffs)

plt.ylabel('Amplitude')
plt.title('Fourier Transform')

# ------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

# ------------------------------- Beginning of Matplotlib helper code -----------------------

def draw_figure(canvas, figure, loc=(0, 0)):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

                # ------------------------------- Beginning of GUI CODE -------------------------------
sg.theme('Light Brown 3')

fig = plt.gcf()  # if using Pyplot then get the figure from the plot
figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

# define the window layout
layout = [[sg.Text('Plot test', font='Any 18')],
                  [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
                            [sg.OK(pad=((figure_w / 2, 0), 3), size=(4, 2))]]

# create the form and show it without the plot
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
            layout, force_toplevel=True, finalize=True)

# add the plot to the window
fig_photo = draw_figure(window['-CANVAS-'].TKCanvas, fig)

# show it all again and get buttons
event, values = window.read()

window.close()
