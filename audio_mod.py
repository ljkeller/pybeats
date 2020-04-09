import os
import sys
from playsound import playsound
from matplotlib import pyplot as plt
import numpy as np
import wave

wd = os.getcwd() + "/"

if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    exit(1)

signal = wave.open(wd + fname, mode='rb')
#Get sampling frequency
fs = signal.getframerate()

print(signal.getnchannels())
print(signal.getnframes())

# WAV files allocate 16 bits per sample
# Readframes(-1) reads all availible data from file
data = np.frombuffer(signal.readframes(-1), dtype="int16")
n_data = data.size
print(len(data))
print(max(data))
print(data)

# Calculate time from samples
t = np.linspace(0, n_data / fs, num=len(data))
print(max(t))
plt.figure("Signal Wave")
plt.plot(t, data)

plt.figure()
Xks = np.fft.rfft(data)

#W axis
omegas = np.fft.rfftfreq(n_data, 1./fs)
plt.plot(omegas, Xks)

plt.show()
