from scipy.io import wavfile
from scipy.signal import resample
from sounddevice import rec, wait
from datetime import datetime
import numpy as np
import json
from time import sleep
import sounddevice as sd


with open("./sensor_info.json","r") as si:
    sidict = json.load(si)
    seconds = sidict["collect_duration"]
    samplerate = sidict["sample_rate"]
    data_path = sidict["data_path"]
    sensor_name = sidict["sensor_name"]
         



def record():
    """
    Record wav files and save them
    """
    while True:
        start_time = datetime.now().timestamp()
        defualt_in= sd.query_devices(sd.default.device[0])
        device_sample_rate = defualt_in["default_samplerate"]
        recorder = rec(frames=int(seconds*device_sample_rate), samplerate=device_sample_rate,channels=1)
        wait()
        recorder = resample(x=recorder,num=int(samplerate*seconds))
        wavfile.write(filename=f"{data_path}{sensor_name}_{start_time}.wav",
                    rate=samplerate,
                    data = recorder
                    )

if __name__ == "__main__":
    record()