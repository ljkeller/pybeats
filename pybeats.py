import time
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import os
from playsound import playsound
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import wave
import threading

matplotlib.use('TkAgg')
sg.theme("Dark Black")

PRI_PURP = "#8A2BE2"
AUD_FREQ = 20000
FIG_H, FIG_W = 500, 500

def useful_freqs(omegas, fourier_coeffs, cutoff):
    tracker = 0
    for i in range(0, omegas.size):
        if abs(fourier_coeffs[i].real) > cutoff or abs(fourier_coeffs[i].imag) > cutoff:
            tracker = i
    return tracker

def draw_figure(canvas, figure, loc=(0,0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both')
    return figure_canvas_agg

# plot with various axes scales
plt.figure(1)
plt.axis('off')
plt.margins(0.01)
plt.tight_layout()
plt.ion()
fig = plt.gcf()
figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

ls = os.listdir("/Users/lucaskeller/code/py/pybeats/54__sleep__guitar/")
ls.sort()
ls = list(filter(lambda f: f.endswith(".wav"), ls))

# All this inside window
layout = [    [sg.Text("PyBeats", font="Any 24", text_color=PRI_PURP)],
              [sg.Listbox(ls, size=(30, 26), font="Any 14",
                  key='-File Path-', background_color=PRI_PURP), 
                  sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
              [sg.Text("What file do you want to modify?", font="Any 14")],
              [sg.Input(size=(45,1), background_color="white", text_color=PRI_PURP,
                  font="Any 14"), 
                  sg.FileBrowse(file_types=(("ALL Files", "*.wav"),), font="Any 14"),
                  sg.Button('Play', button_color=("white", PRI_PURP), font="Any 14"), 
                  sg.Button('Base Boost', button_color=("white", PRI_PURP), font="Any 14"),
                  sg.Button('Mid Boost', button_color=("white", PRI_PURP), font="Any 14"),
                  sg.Button('Cancel', font="Any 14")]   
        ]

# Create the window
win_name = "Py Beats (" + os.getcwd() + ")"
window = sg.Window(win_name, layout, finalize=True, button_color=PRI_PURP)
fig_visualizer = draw_figure(window['-CANVAS-'].TKCanvas, fig)

#setup audio thread
# Event loop to process events
while True:
    event, values = window.read()
    print("Hello")
    if event in (None, 'Cancel'):
        break
    if event == "Play":
        if values['-File Path-']:
            #print(os.getcwd() + "/54__slee__guitar/" + values['-File Path-'][0])
            fpath = os.getcwd() + "/54__sleep__guitar/" + values['-File Path-'][0]
            audio_thread = threading.Thread(target=playsound, args=(fpath,))

            # Aquire signal
            signal = wave.open(fpath, mode='rb')
            fs = signal.getframerate()
            signal = np.frombuffer(signal.readframes(-1), dtype='int16')
            n_samples = signal.size
            n_signal = signal.size
            print(n_signal * 1./fs)
            
            # Identify time axis and number of play loops
            t = np.linspace(0, n_signal / fs, num=n_signal)
            n_loops = int(5 * t[-1])

            # get fourier coeffs
            fourier_coeffs = np.fft.rfft(signal)
            omegas = np.fft.rfftfreq(n_signal, 1./fs)
            n_omegas = omegas.size

            max_mag = max(max(fourier_coeffs.real), max(fourier_coeffs.imag))

            audio_thread.start()
            audio_tid = audio_thread.native_id
            start_time = time.time()
            for i in range(0, n_loops):
                # Break signal up into chunks for live analysis
                start = int(i * n_samples//n_loops)
                end = int((i + 1) * n_samples//n_loops)

                #re-establish fouier coeffs
                n_signal = len(signal[start:end])
                fourier_coeffs = np.fft.rfft(signal[start:end])
                omegas = np.fft.rfftfreq(n_signal, 1./fs)

                #live plotting
                fig.clear()
                plt.ylim(-max_mag/10, max_mag/10)
                plt.xscale('log')
                #plt.xticks([1, 10, 100, 1000, 40000, 100000])
                #plt.axis('off')
                plt.margins(0.001)
                plt.plot(omegas, fourier_coeffs.real, PRI_PURP, omegas, fourier_coeffs.imag,
                        PRI_PURP)
                fig_visualizer.draw()
                playtime_ms = ((1./fs) * n_signal) * 1000
                elapsed_time_ms = (time.time() - start_time) * 1000 
                event, values = window.read(timeout=playtime_ms - elapsed_time_ms)
                start_time = time.time()
            
            audio_thread.join()
        else:
            fpath = values[0]
            playsound(fpath)
            print(event)
            print('You entered ', values[0])

