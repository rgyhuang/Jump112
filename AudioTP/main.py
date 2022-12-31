import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import wave
# may use later
#from pyqtgraph.Qt import QtGui, QtCore
#import pyqtgraph as pg
import struct
from scipy.fftpack import fft
import sys
import time

# based on audio visualization YouTube series by Mark Jay:
# https://www.youtube.com/playlist?list=PLX-LrBk6h3wQVsrldsQdtKmeTygurKiuS
class AudioSpectrum(object):
    
    def __init__(self):
        # audio stream constants
        # smaller sampleSize less info, but more performance
        self.chunkSize = 1024*2
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sampleRate = 44100
        self.pause = False
        self.wf = wave.open('test.wav', 'rb')
        
        # # create audio stream object
        # self.audio = pyaudio.PyAudio()
        # self.stream = self.audio.open(
        # format=self.format, 
        # channels=self.channels,
        # rate=self.sampleRate,
        # input=True,
        # output=True,
        # frames_per_buffer=self.chunkSize)

        # read audio from file

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format = self.audio.get_format_from_width(self.wf.getsampwidth()),
                channels = self.wf.getnchannels(),
                rate = self.wf.getframerate(),
                output = True)

        self.init_plots()
        self.start_plot()

    def init_plots(self):
        plt.ion()
        # x variables
        x = np.arange(0, 2 * self.chunkSize, 2)
        self.xft = np.linspace(0, self.sampleRate, self.chunkSize)

        # matplotlib figure and axes
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, figsize=(15,7))
        # create a line object with random data (wave form)
        self.line, = self.ax1.plot(x, np.random.rand(self.chunkSize), '-', lw=2)
        # scatter plot sound blob thingies
        a = np.linspace(-1, 1, self.chunkSize)
        c = np.tan(a)
        
        ## testing dynamic 3D scatter plot
        # self.fig = plt.figure()
        # self.ax2 = fig.add_subplot(projection='3d')
        # self.ax2.scatter(self.xft, np.,random.rand(self.chunkSize), 1)

        # format spectrum axes
        self.ax2.set_xlim(20, self.sampleRate / 2)
        self.sc = self.ax2.scatter(self.xft, 
            np.random.rand(self.chunkSize), c=c, marker='o')
        
        # create semilogx line for spectrum (line)
        #self.line_fft, = self.ax2.semilogx(self.xft, np.random.rand(self.chunkSize), '-', lw=2)
        
        # format waveform axes
        self.ax1.set_title('AUDIO WAVEFORM')
        self.ax1.set_xlabel('samples')
        self.ax1.set_ylabel('volume')
        self.ax1.set_ylim(0, 255)
        self.ax1.set_xlim(0, 2 * self.chunkSize)
        
        plt.setp(
            self.ax1, yticks=[0, 128, 255],
            xticks=[0, self.chunkSize, 2 * self.chunkSize],
        )
        plt.setp(self.ax2, yticks=[0, 1],)

 
        self.ax2.set_xscale('log')
        plt.show(block=False)

    def start_plot(self):

        while not self.pause or data != '':
            # data = self.wf.readframes(self.chunkSize)
            # data_int = struct.unpack(str(2 * self.chunkSize) + 'B', data)
            # data_np = np.array(data_int, dtype='b')[::2] + 128
            data = self.wf.readframes(self.chunkSize)
            self.stream.write(data)
            data_int = struct.unpack(str(2 * self.chunkSize) + 'h', data)
            data_np = np.array(data_int, dtype='b')[::2] + 128
            self.line.set_ydata(data_np)
            
            # compute FFT and update line
            yf = fft(data_int)
            # frequency spectrum using fft line
            #self.line_fft.set_ydata(
             # np.abs(yf[0:self.chunkSize]) / (128 * self.chunkSize))

            # update scatter plot dots, looks cool lmao
            self.sc.set_offsets(np.c_[self.xft, 
                      np.abs(yf[0:self.chunkSize]) / (128 * self.chunkSize)])

            # update figure canvas
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def exit_app(self):
        print('stream closed')
        self.p.close(self.stream)
        
    def onClick(self, event):
        self.pause = True

if __name__ == '__main__':
    AudioSpectrum()