#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import sys
import getopt
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from scipy import signal

class SleepEEG:
    def __init__(self):
        s = 2.5/256/1000 # rough guess
        v = np.loadtxt("eeg_c.dat")[:,0]
        v = v * s
        self.fs = 1.0/0.003
        # highpass Butterworth filter
        cutoff = 0.25
        # create a 4th order highpass
        b, a = signal.butter(2, cutoff/self.fs*2.0, 'highpass')
        # filter the signal adc1
        v = signal.lfilter(b, a, v)
        # create a 2nd order order stopband filter at 50Hz
        # to remove the 50Hz mains
        f1 = 45
        f2 = 55
        b, a = signal.butter(2, [f1/self.fs*2.0, f2/self.fs*2.0 ], 'bandstop')
        # filter the 1st ADC channel
        self.data = signal.lfilter(b, a, v)

    def getTimeAxis(self):
        return np.linspace(0,(len(self.data)/self.fs),len(self.data))

    def getDateTimeAndData(self):
        ts = []
        d = []
        customdate = datetime.datetime(2023, 1, 1, 0, 0)
        for i in range(len(self.data)):
            ts.append(customdate)
            customdate = customdate + datetime.timedelta(seconds=1.0/self.fs)
            d.append(self.data[i])
        return ts,d

    def getData(self):
        return self.data
        

eeg = SleepEEG()
t,y = eeg.getDateTimeAndData()
plt.plot(t,y)
plt.xlabel("time/secs")
plt.ylabel("EEG/volt")
plt.show()
