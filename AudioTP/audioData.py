import numpy as np
import pyaudio
import struct
from scipy.fftpack import fft
from scipy.io.wavfile import read
import sys
import time
import wave

class AudioStream(object):
    def __init__(self):        
        self.chunkSize = 2048*4
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sampleRate, self.data = read('audio.wav')
        self.pause = False
        self.wf = wave.open('audio.wav', 'rb')
        self.xft = np.linspace(0, self.sampleRate, self.chunkSize)
        self.duration = len(self.data)/self.sampleRate
        self.time = np.arange(0, self.duration, 1/self.sampleRate)
        #self.stft = np.abs(fft.stft(self.time, fs=512, nfft=self.chunkSize))
        # self.audio = pyaudio.PyAudio()
        # self.stream = self.audio.open(
        #         format=self.format, 
        #         channels=self.channels,
        #         rate=self.sampleRate,
        #         input=True,
        #         output=True,
        #         frames_per_buffer=self.chunkSize)

        # read audio from file
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format = self.audio.get_format_from_width(self.wf.getsampwidth()),
                channels = self.wf.getnchannels(),
                rate = self.wf.getframerate(),
                output = True)

    def getData(self):
        self.data = self.wf.readframes(self.chunkSize)
        self.stream.write(self.data)
        data_int = struct.unpack(str(2 * self.chunkSize) + 'h', self.data)
        data_np = np.array(data_int, dtype='b')[::2] + 128
        f = fft(data_int)
        translateF = np.c_[self.xft, 
                      np.abs(f[0:self.chunkSize]) / (128 * self.chunkSize)]
        translateF = np.log10(translateF)
        return translateF