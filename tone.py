from sounddevice import play, wait
import numpy as np
from scipy.io import wavfile
x= np.arange(0,30,1/48000)
f=np.linspace(10,20000,48000*30)
y = np.sin(2*np.pi*x*f)
play(y,samplerate=16000)
wait()
# wavfile.write("sine progression.wav",48000,y)