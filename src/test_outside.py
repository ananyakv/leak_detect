#!/usr/bin/python3
'''
import pyaudio
import wave
import datetime
import time
import os
import RPi.GPIO as GPIO
import sounddevice as sd
import soundfile as sf
#import requests
#import json
'''
import pyaudio
import wave
import datetime
import time
import os
#from script 2:
from scipy.io import wavfile
from scipy.fftpack import fft
import numpy as np
import glob
import os
import RPi.GPIO as GPIO
import time
import pyaudio
import wave
import sounddevice as sd
import soundfile as sf
import RPi.GPIO as GPIO
import requests
import json

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 8192
RECORD_SECONDS = 10
RECORD_PERIODS = 5

API_KEY = 'o.F6iN9x3T5spuMqBgaIbKCcuWDAxk1DFj'
#change to 10 sec to see if messaging works (difficulty with pushbullet)

def pushMessage(title, body):
    data = {

        'type':'note',

        'title':title,

        'body':body        }
    resp = requests.post('https://api.pushbullet.com/api/pushes',data=data, auth=(API_KEY,''))

def record_audio(format, channels, rate, seconds, frames_per_buffer):
    """
    Records audio for a set number of seconds, and saves it to the output directory
    """
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=frames_per_buffer)

    # start Recording
    print("recording")
    frames = []
    for i in range(0, int(rate / frames_per_buffer * seconds)):
        data = stream.read(frames_per_buffer, exception_on_overflow = False)
        frames.append(data)

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("stop recording")
    # get name and locaton of file to create
    filename = getOutputDirectory() + getFileName()
    # write data to audio file
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(audio.get_sample_size(format))
    wave_file.setframerate(rate)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

def getOutputDirectory():
        """
        Returns the name of the output directory, creating it if it does not exist
        """
        directory = "/home/pi/"
        now = datetime.datetime.now()
        directory_format = "%Y%m%d"
        directory += "testing_files" + now.strftime(directory_format) + "/"
        # if directory doesn't exist, create it
        if not os.path.exists(directory):
                os.mkdir(directory)
        return directory

def getFileName():
        """
        Generates a name for a file, based on current time of form 'audio_HHMMSS.wav'
        """
        filename = "audio_"
        now = datetime.datetime.now()
        filename_format = "%H%M%S"
        print(filename + now.strftime(filename_format) + ".wav")
        return filename + now.strftime(filename_format) + ".wav"

for i in range(RECORD_PERIODS):

        # record audio
        print("recording")
        pushMessage("recording!", "test is about to start")
        record_audio(FORMAT, CHANNELS, RATE, RECORD_SECONDS, CHUNK)
        time.sleep(5)