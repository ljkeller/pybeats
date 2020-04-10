#!/usr/bin/env python
import time
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

NUM_LOOPS = 100 

def useful_freqs(omegas, fourier_coeffs):
    tracker = 0;
    for i in range(0, omegas.size):
        if abs(fourier_coeffs[i].real) > 1000000 or abs(fourier_coeffs[i].imag) > 1000000:
            tracker = i
    return tracker

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
NUM_LOOPS = int(10 * t[-1])
print(NUM_LOOPS)

fourier_coeffs = np.fft.rfft(signal)
omegas = np.fft.rfftfreq(n_signal, 1./fs)
n_omegas = omegas.size

max_magr = max(fourier_coeffs.real)
max_magi = max(fourier_coeffs.imag)
max_mag = max(max_magr, max_magi)
#fourier_coeffs = fourier_coeffs / max(max_mag)
#fourier_coeffs.imag = fourier_coeffs.imag / max(max_mag)

max_w = useful_freqs(omegas, fourier_coeffs)

plt.figure()
plt.ion()
plt.plot(omegas, fourier_coeffs)
plt.ylabel('Amplitude')
plt.title('Fourier Transform')
plt.ylim(-10, 10)
plt.xlim(0, 10000)

# ------------------------------- END OF YOUR MATPLOTLIB CODE -------------------------------

# ------------------------------- Beginning of Matplotlib helper code -----------------------

def draw_figure(canvas, figure, loc=(0, 0)):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both')
        return figure_canvas_agg

                # ------------------------------- Beginning of GUI CODE -------------------------------
sg.theme('Black')

fig = plt.gcf()  # if using Pyplot then get the figure from the plot
figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

# define the window layout
layout = [[sg.Text('Plot test', font='Any 18')],
                  [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
                            [sg.OK(pad=((figure_w / 2, 0), 3), size=(4, 2))]]

# create the form and show it without the plot
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
            layout, force_toplevel=True, finalize=True)

fig_photo = draw_figure(window['-CANVAS-'].TKCanvas, fig)

# add the plot to the window
for i in range(0, NUM_LOOPS):
    # Break signal up into chunks for live analysis
    start = int(i * n_omegas/NUM_LOOPS)
    end = int((i + 1) * n_omegas/NUM_LOOPS)

    #Re-establish fourier coeffs
    n_signal = len(signal[start:end])
    fourier_coeffs = np.fft.rfft(signal[start:end])
    omegas = np.fft.rfftfreq(n_signal, 1./fs)
    figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

    #Live plotting
    fig.clear()
    plt.ylim(-max_mag, max_mag)
    plt.xlim(0, max_w)
    plt.plot(omegas, fourier_coeffs.real, 'r', omegas, fourier_coeffs.imag, 'r')
    fig_photo.draw()

    # Initiate window timeout based upon how long graph should be up
    event, values = window.read(timeout=(1./fs)*n_signal * 1000)

# show it all again and get buttons
event, values = window.read(timeout=20)

time.sleep(10)
window.close()


